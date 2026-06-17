from pathlib import Path

import pandas as pd

from fair_ml_cyber.stats import (
    generate_q1_statistics,
    inter_seed_variance,
    paired_split_comparisons,
    summarize_metric,
)


def _results_frame() -> pd.DataFrame:
    rows = []
    for seed, offset in [(42, 0.0), (7, -0.01), (99, 0.01)]:
        for tier in ["no_identity", "deployment_safe"]:
            rows.append(
                {
                    "model": "logistic_regression",
                    "feature_tier": tier,
                    "split": "random_stratified",
                    "seed": seed,
                    "status": "completed",
                    "macro_f1": 0.90 + offset,
                }
            )
            rows.append(
                {
                    "model": "logistic_regression",
                    "feature_tier": tier,
                    "split": "temporal",
                    "seed": seed,
                    "status": "completed",
                    "macro_f1": 0.60 + offset,
                }
            )
    return pd.DataFrame(rows)


def test_summarize_metric_bootstrap_ci():
    summary = summarize_metric(
        _results_frame(),
        metric="macro_f1",
        group_cols=["model", "split"],
        n_boot=100,
    )

    temporal = summary[summary["split"] == "temporal"].iloc[0]
    assert temporal["n"] == 6
    assert 0.58 < temporal["ci_low"] < temporal["mean"] < temporal["ci_high"] < 0.62


def test_paired_split_comparisons_outputs_delta_and_ratio():
    comparisons = paired_split_comparisons(
        _results_frame(),
        metric="macro_f1",
        group_cols=["model"],
        pair_cols=["seed", "feature_tier"],
        n_boot=100,
    )

    row = comparisons.iloc[0]
    assert row["stress_split"] == "temporal"
    assert row["n_pairs"] == 6
    assert round(row["mean_delta"], 6) == -0.3
    assert 0.65 < row["mean_ratio"] < 0.68
    assert row["sign_flip_p_value"] is not None


def test_inter_seed_variance_counts_seeds():
    variance = inter_seed_variance(
        _results_frame(),
        metric="macro_f1",
        group_cols=["model", "feature_tier", "split"],
    )

    assert set(variance["n_seeds"]) == {3}
    assert variance["inter_seed_std"].gt(0).all()


def test_generate_q1_statistics_writes_outputs(tmp_path):
    input_path = tmp_path / "results.csv"
    _results_frame().to_csv(input_path, index=False)

    metadata = generate_q1_statistics(
        [input_path],
        tmp_path / "stats",
        metric="macro_f1",
        n_boot=50,
    )

    for path in metadata["outputs"].values():
        assert Path(path).exists()

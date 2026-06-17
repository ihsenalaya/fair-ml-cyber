import json
from pathlib import Path

import pandas as pd

from fair_ml_cyber.advanced import run_advanced_analysis


def test_run_advanced_analysis_writes_expected_artifacts(tmp_path):
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    labels = ["Benign", "DoS_Hulk", "Web_XSS"]
    rows = []
    for i in range(90):
        label = labels[i % len(labels)]
        rows.append(
            {
                "flow_id": f"f{i}",
                "timestamp": f"2017-07-{1 + (i // 30):02d} 00:00:{i % 60:02d}",
                "src_ip": f"10.0.0.{i % 5}",
                "src_port": 1000 + i,
                "dst_ip": f"10.0.1.{i % 3}",
                "dst_port": 80 + (i % 2),
                "protocol": 6,
                "duration": float(i + 1),
                "packets_count": i + 2,
                "payload_bytes_mean": 100.0 + i,
                "label": label,
            }
        )
    pd.DataFrame(rows[:45]).to_csv(csv_dir / "part1.csv", index=False)
    pd.DataFrame(rows[45:]).to_csv(csv_dir / "part2.csv", index=False)

    summary = run_advanced_analysis(
        csv_dir,
        tmp_path / "work",
        seed=3,
        models=["hist_gradient_boosting"],
        feature_tiers=["deployment_safe"],
        split_protocols=["random_stratified"],
        unknown_families=["Web"],
        result_prefix="unit_adv",
        explain_sample_size=10,
        permutation_repeats=1,
    )

    assert summary["binary_runs"] == 1
    assert summary["multiclass_runs"] == 1
    assert summary["open_set_runs"] == 1
    for path in summary["outputs"].values():
        assert Path(path).exists()

    summary_path = tmp_path / "work" / "advanced_results" / "unit_adv_summary.json"
    with open(summary_path, encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["binary_runs"] == 1

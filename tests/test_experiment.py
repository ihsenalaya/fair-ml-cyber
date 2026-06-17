import os

import pandas as pd

from fair_ml_cyber.experiment import run_experiment, setup_mlflow


def test_setup_mlflow_clears_parent_run_environment(tmp_path):
    os.environ["MLFLOW_RUN_ID"] = "azure-parent-run"
    os.environ["MLFLOW_EXPERIMENT_ID"] = "azure-experiment"

    setup_mlflow(tmp_path)

    assert "MLFLOW_RUN_ID" not in os.environ
    assert os.environ.get("MLFLOW_EXPERIMENT_ID") != "azure-experiment"


def test_run_experiment_writes_results_and_events(tmp_path):
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    rows = []
    for i in range(40):
        rows.append(
            {
                "flow_id": f"f{i}",
                "timestamp": f"2017-07-{1 + (i // 20):02d} 00:00:{i % 60:02d}",
                "src_ip": f"10.0.0.{i % 5}",
                "src_port": 1000 + i,
                "dst_ip": f"10.0.1.{i % 3}",
                "dst_port": 80,
                "protocol": 6,
                "duration": float(i + 1),
                "packets_count": i + 2,
                "payload_bytes_mean": 100.0 + i,
                "label": "Benign" if i % 2 == 0 else "DoS_Hulk",
            }
        )
    pd.DataFrame(rows[:20]).to_csv(csv_dir / "part1.csv", index=False)
    pd.DataFrame(rows[20:]).to_csv(csv_dir / "part2.csv", index=False)

    summary = run_experiment(
        csv_dir,
        tmp_path / "work",
        models=["hist_gradient_boosting"],
        feature_tiers=["deployment_safe"],
        split_protocols=["random_stratified"],
        result_prefix="unit",
        save_models=False,
        save_prepared_data=False,
    )

    results_path = tmp_path / "work" / "results" / "unit_results.csv"
    events_path = tmp_path / "work" / "results" / "unit_events.jsonl"
    results = pd.read_csv(results_path)

    assert summary["runs"] == 1
    assert summary["completed_runs"] == 1
    assert summary["failed_runs"] == 0
    assert summary["prepared_path"] is None
    assert summary["results_path"] == str(results_path)
    assert events_path.exists()
    assert not (tmp_path / "work" / "processed" / "full.parquet").exists()
    assert results.loc[0, "status"] == "completed"
    assert results.loc[0, "n_train"] > 0
    assert "experiment_completed" in events_path.read_text(encoding="utf-8")

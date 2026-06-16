import os

from fair_ml_cyber.experiment import setup_mlflow


def test_setup_mlflow_clears_parent_run_environment(tmp_path):
    os.environ["MLFLOW_RUN_ID"] = "azure-parent-run"
    os.environ["MLFLOW_EXPERIMENT_ID"] = "azure-experiment"

    setup_mlflow(tmp_path)

    assert "MLFLOW_RUN_ID" not in os.environ
    assert os.environ.get("MLFLOW_EXPERIMENT_ID") != "azure-experiment"

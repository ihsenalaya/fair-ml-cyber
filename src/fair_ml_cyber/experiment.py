"""Experiment orchestration."""

from __future__ import annotations

import json
from pathlib import Path

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.data import load_csvs, save_prepared
from fair_ml_cyber.features import make_xy, select_feature_tier
from fair_ml_cyber.hashing import hash_dataframe, hash_object
from fair_ml_cyber.metrics import binary_metrics, metrics_to_frame, save_json
from fair_ml_cyber.modeling import fit_predict, save_model
from fair_ml_cyber.plots import plot_label_distribution, plot_metric_by_split
from fair_ml_cyber.splits import (
    day_holdout_split,
    endpoint_pair_holdout_split,
    random_split,
    scenario_holdout_split,
    temporal_split,
)


def setup_mlflow(work_dir: str | Path) -> None:
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(f"sqlite:///{(work_dir / 'mlflow.db').resolve()}")
    client = MlflowClient()
    experiment_name = "fair-ml-cyber"
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        client.create_experiment(
            experiment_name,
            artifact_location=(work_dir / "mlartifacts").resolve().as_uri(),
        )
    mlflow.set_experiment(experiment_name)


def run_smoke(
    csv_dir: str | Path,
    work_dir: str | Path,
    sample_per_file: int = 2000,
    seed: int = 42,
) -> dict:
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    setup_mlflow(work_dir)

    audit = audit_csv_dir(csv_dir, work_dir / "audit")
    plot_label_distribution(work_dir / "audit" / "label_distribution.csv", work_dir / "figures" / "labels.png")

    df = load_csvs(csv_dir, sample_per_file=sample_per_file, random_state=seed)
    prepared_path = work_dir / "processed" / "sample.parquet"
    save_prepared(df, prepared_path)
    data_hash = hash_dataframe(df)

    split_objects = [random_split(df, target="label", seed=seed), temporal_split(df)]
    available_days = sorted(d for d in df["day"].dropna().unique().tolist() if d != "NaT")
    if available_days:
        split_objects.append(day_holdout_split(df, holdout_day=available_days[-1], seed=seed))
    if "Web" in set(df["attack_family"]):
        split_objects.append(scenario_holdout_split(df, holdout_family="Web", seed=seed))
    try:
        split_objects.append(endpoint_pair_holdout_split(df, seed=seed))
    except ValueError:
        pass

    feature_tiers = ["no_identity", "deployment_safe"]
    models = ["logistic_regression", "random_forest", "hist_gradient_boosting"]
    results: list[dict] = []

    for tier in feature_tiers:
        feature_info = select_feature_tier(df, tier)
        feature_hash = hash_object({"tier": tier, "columns": feature_info.columns})
        X_all, y_all, _ = make_xy(df, tier=tier, target="binary_label")
        for split in split_objects:
            X_train = X_all.loc[split.train_idx]
            y_train = y_all.loc[split.train_idx]
            X_test = X_all.loc[split.test_idx]
            y_test = y_all.loc[split.test_idx]
            for model_name in models:
                run_name = f"smoke-{model_name}-{tier}-{split.name}"
                with mlflow.start_run(run_name=run_name):
                    mlflow.log_params(
                        {
                            "model": model_name,
                            "feature_tier": tier,
                            "split": split.name,
                            "seed": seed,
                            "sample_per_file": sample_per_file,
                            "data_hash": data_hash,
                            "feature_hash": feature_hash,
                            "split_hash": split.split_hash,
                            "n_train": len(X_train),
                            "n_test": len(X_test),
                            "n_features": len(feature_info.columns),
                        }
                    )
                    fit = fit_predict(model_name, X_train, y_train, X_test, seed=seed)
                    if fit.y_prob is None:
                        y_prob = fit.y_pred.astype(float)
                    else:
                        y_prob = fit.y_prob
                    metrics = binary_metrics(y_test.to_numpy(), y_prob)
                    mlflow.log_metrics(
                        {
                            k: float(v)
                            for k, v in metrics.items()
                            if isinstance(v, (int, float)) and v is not None
                        }
                    )
                    mlflow.log_metric("train_seconds", fit.train_seconds)
                    mlflow.log_metric("inference_seconds", fit.inference_seconds)

                    model_path = work_dir / "models" / f"{run_name}.joblib"
                    save_model(fit.model, model_path)
                    mlflow.log_artifact(str(model_path))

                    row = {
                        "model": model_name,
                        "feature_tier": tier,
                        "split": split.name,
                        "seed": seed,
                        "data_hash": data_hash,
                        "feature_hash": feature_hash,
                        "split_hash": split.split_hash,
                        "n_train": len(X_train),
                        "n_test": len(X_test),
                        "n_features": len(feature_info.columns),
                        "train_seconds": fit.train_seconds,
                        "inference_seconds": fit.inference_seconds,
                        **metrics,
                    }
                    results.append(row)

    results_df = metrics_to_frame(results)
    results_path = work_dir / "results" / "smoke_results.csv"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(results_path, index=False)
    plot_metric_by_split(results_path, work_dir / "figures" / "macro_f1_by_split.png")

    summary = {
        "audit": {
            "num_files": audit["num_files"],
            "total_rows": audit["total_rows"],
            "data_hash": audit["data_hash"],
        },
        "sample_rows": len(df),
        "results_path": str(results_path),
        "runs": len(results),
    }
    save_json(summary, work_dir / "results" / "smoke_summary.json")
    with open(work_dir / "results" / "smoke_summary.json", encoding="utf-8") as f:
        return json.load(f)

"""Experiment orchestration."""

from __future__ import annotations

import json
import os
from collections.abc import Sequence
from datetime import datetime, timezone
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


DEFAULT_SPLIT_PROTOCOLS = [
    "random_stratified",
    "temporal",
    "latest_day_holdout",
    "scenario_holdout_Web",
    "endpoint_pair_holdout",
]
DEFAULT_FEATURE_TIERS = ["no_identity", "deployment_safe"]
DEFAULT_MODELS = ["logistic_regression", "random_forest", "hist_gradient_boosting"]


def setup_mlflow(work_dir: str | Path) -> None:
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    for env_name in ("MLFLOW_RUN_ID", "MLFLOW_EXPERIMENT_ID"):
        os.environ.pop(env_name, None)
    mlflow.end_run()
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log_event(log_path: Path, event: str, **payload) -> None:
    row = {"timestamp_utc": _utc_now(), "event": event, **payload}
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, default=str) + "\n")
    print(json.dumps(row, default=str), flush=True)


def _build_splits(
    df: pd.DataFrame,
    split_protocols: Sequence[str],
    seed: int = 42,
) -> tuple[list, list[dict]]:
    split_objects = []
    skipped: list[dict] = []

    for protocol in split_protocols:
        try:
            if protocol == "random_stratified":
                split_objects.append(random_split(df, target="label", seed=seed))
            elif protocol == "temporal":
                split_objects.append(temporal_split(df))
            elif protocol == "latest_day_holdout":
                available_days = sorted(
                    d for d in df["day"].dropna().unique().tolist() if d != "NaT"
                )
                if not available_days:
                    raise ValueError("No valid day values are available")
                split_objects.append(day_holdout_split(df, holdout_day=available_days[-1], seed=seed))
            elif protocol == "scenario_holdout_Web":
                split_objects.append(scenario_holdout_split(df, holdout_family="Web", seed=seed))
            elif protocol == "endpoint_pair_holdout":
                split_objects.append(endpoint_pair_holdout_split(df, seed=seed))
            else:
                raise ValueError(f"Unknown split protocol: {protocol}")
        except ValueError as exc:
            skipped.append({"split_protocol": protocol, "reason": str(exc)})

    if not split_objects:
        raise ValueError(f"No split protocols could be built; skipped={skipped}")
    return split_objects, skipped


def run_experiment(
    csv_dir: str | Path,
    work_dir: str | Path,
    *,
    sample_per_file: int | None = None,
    seed: int = 42,
    models: Sequence[str] | None = None,
    feature_tiers: Sequence[str] | None = None,
    split_protocols: Sequence[str] | None = None,
    result_prefix: str = "experiment",
    save_models: bool = True,
    save_prepared_data: bool = True,
) -> dict:
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    setup_mlflow(work_dir)

    models = list(models or DEFAULT_MODELS)
    feature_tiers = list(feature_tiers or DEFAULT_FEATURE_TIERS)
    split_protocols = list(split_protocols or DEFAULT_SPLIT_PROTOCOLS)
    results_dir = work_dir / "results"
    events_path = results_dir / f"{result_prefix}_events.jsonl"
    if events_path.exists():
        events_path.unlink()

    _log_event(
        events_path,
        "experiment_start",
        result_prefix=result_prefix,
        sample_per_file=sample_per_file,
        seed=seed,
        models=models,
        feature_tiers=feature_tiers,
        split_protocols=split_protocols,
        save_models=save_models,
        save_prepared_data=save_prepared_data,
    )

    audit = audit_csv_dir(csv_dir, work_dir / "audit")
    plot_label_distribution(work_dir / "audit" / "label_distribution.csv", work_dir / "figures" / "labels.png")

    df = load_csvs(csv_dir, sample_per_file=sample_per_file, random_state=seed)
    prepared_path = None
    if save_prepared_data:
        prepared_name = "sample.parquet" if sample_per_file else "full.parquet"
        prepared_path = work_dir / "processed" / prepared_name
        save_prepared(df, prepared_path)
    data_hash = hash_dataframe(df)

    split_objects, skipped_splits = _build_splits(df, split_protocols, seed=seed)
    for skipped in skipped_splits:
        _log_event(events_path, "split_skipped", **skipped)

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
                run_name = f"{result_prefix}-{model_name}-{tier}-{split.name}"
                base_row = {
                    "experiment": result_prefix,
                    "model": model_name,
                    "feature_tier": tier,
                    "split": split.name,
                    "seed": seed,
                    "sample_per_file": sample_per_file,
                    "data_hash": data_hash,
                    "feature_hash": feature_hash,
                    "split_hash": split.split_hash,
                    "n_train": len(X_train),
                    "n_val": len(split.val_idx),
                    "n_test": len(X_test),
                    "n_features": len(feature_info.columns),
                    "train_positive_rate": float(y_train.mean()) if len(y_train) else None,
                    "test_positive_rate": float(y_test.mean()) if len(y_test) else None,
                }
                _log_event(events_path, "run_start", run_name=run_name, **base_row)
                try:
                    with mlflow.start_run(run_name=run_name):
                        mlflow.log_params(base_row)
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

                        model_path = None
                        if save_models:
                            model_path = work_dir / "models" / f"{run_name}.joblib"
                            save_model(fit.model, model_path)
                            mlflow.log_artifact(str(model_path))

                    row = {
                        **base_row,
                        "status": "completed",
                        "train_seconds": fit.train_seconds,
                        "inference_seconds": fit.inference_seconds,
                        "model_path": str(model_path) if model_path else None,
                        "error_type": None,
                        "error_message": None,
                        **metrics,
                    }
                    results.append(row)
                    _log_event(
                        events_path,
                        "run_completed",
                        run_name=run_name,
                        train_seconds=fit.train_seconds,
                        inference_seconds=fit.inference_seconds,
                        macro_f1=metrics.get("macro_f1"),
                        auroc=metrics.get("auroc"),
                    )
                except Exception as exc:
                    row = {
                        **base_row,
                        "status": "failed",
                        "train_seconds": None,
                        "inference_seconds": None,
                        "model_path": None,
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    }
                    results.append(row)
                    _log_event(
                        events_path,
                        "run_failed",
                        run_name=run_name,
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )

    results_df = metrics_to_frame(results)
    results_path = results_dir / f"{result_prefix}_results.csv"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(results_path, index=False)
    if "macro_f1" in results_df and results_df["macro_f1"].notna().any():
        plot_metric_by_split(results_path, work_dir / "figures" / "macro_f1_by_split.png")

    summary = {
        "audit": {
            "num_files": audit["num_files"],
            "total_rows": audit["total_rows"],
            "data_hash": audit["data_hash"],
        },
        "sample_rows": len(df),
        "prepared_path": str(prepared_path) if prepared_path else None,
        "results_path": str(results_path),
        "events_path": str(events_path),
        "runs": len(results),
        "completed_runs": int((results_df["status"] == "completed").sum()) if "status" in results_df else 0,
        "failed_runs": int((results_df["status"] == "failed").sum()) if "status" in results_df else 0,
        "skipped_splits": skipped_splits,
    }
    summary_path = results_dir / f"{result_prefix}_summary.json"
    save_json(summary, summary_path)
    _log_event(events_path, "experiment_completed", **summary)
    with open(summary_path, encoding="utf-8") as f:
        return json.load(f)


def run_smoke(
    csv_dir: str | Path,
    work_dir: str | Path,
    sample_per_file: int = 2000,
    seed: int = 42,
) -> dict:
    return run_experiment(
        csv_dir,
        work_dir,
        sample_per_file=sample_per_file,
        seed=seed,
        models=DEFAULT_MODELS,
        feature_tiers=DEFAULT_FEATURE_TIERS,
        split_protocols=DEFAULT_SPLIT_PROTOCOLS,
        result_prefix="smoke",
    )

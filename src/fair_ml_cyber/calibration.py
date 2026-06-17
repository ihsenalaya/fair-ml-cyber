"""Post-hoc calibration baseline experiments."""

from __future__ import annotations

import json
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.data import load_csvs
from fair_ml_cyber.experiment import DEFAULT_SPLIT_PROTOCOLS, _build_splits, _log_event
from fair_ml_cyber.features import make_xy, select_feature_tier
from fair_ml_cyber.hashing import hash_dataframe, hash_object
from fair_ml_cyber.metrics import binary_metrics, save_json
from fair_ml_cyber.modeling import fit_predict


DEFAULT_CALIBRATION_MODELS = ["logistic_regression", "hist_gradient_boosting"]
DEFAULT_CALIBRATION_FEATURE_TIERS = ["deployment_safe"]


def _has_two_classes(y: pd.Series) -> bool:
    return y.astype(int).nunique(dropna=False) >= 2


def _platt_calibrate(
    y_val: pd.Series,
    val_prob: np.ndarray,
    test_prob: np.ndarray,
    seed: int,
) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    model = LogisticRegression(max_iter=1000, random_state=seed)
    model.fit(np.asarray(val_prob).reshape(-1, 1), y_val.astype(int))
    calibrated = model.predict_proba(np.asarray(test_prob).reshape(-1, 1))[:, 1]
    return calibrated.astype(float), time.perf_counter() - start


def _isotonic_calibrate(
    y_val: pd.Series,
    val_prob: np.ndarray,
    test_prob: np.ndarray,
) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    model = IsotonicRegression(out_of_bounds="clip")
    model.fit(np.asarray(val_prob, dtype=float), y_val.astype(int).to_numpy())
    calibrated = model.predict(np.asarray(test_prob, dtype=float))
    return np.asarray(calibrated, dtype=float), time.perf_counter() - start


def _metric_row(
    base: dict[str, Any],
    *,
    calibration_method: str,
    y_test: pd.Series,
    y_prob: np.ndarray,
    calibration_seconds: float,
) -> dict[str, Any]:
    return {
        **base,
        "calibration_method": calibration_method,
        "calibration_seconds": calibration_seconds,
        **binary_metrics(y_test.to_numpy(), y_prob),
    }


def run_calibration_baselines(
    csv_dir: str | Path,
    work_dir: str | Path,
    *,
    sample_per_file: int | None = None,
    seed: int = 42,
    models: Sequence[str] | None = None,
    feature_tiers: Sequence[str] | None = None,
    split_protocols: Sequence[str] | None = None,
    result_prefix: str = "calibration_baselines",
) -> dict[str, Any]:
    work_dir = Path(work_dir)
    results_dir = work_dir / "calibration_results"
    results_dir.mkdir(parents=True, exist_ok=True)
    events_path = results_dir / f"{result_prefix}_events.jsonl"
    if events_path.exists():
        events_path.unlink()

    models = list(models or DEFAULT_CALIBRATION_MODELS)
    feature_tiers = list(feature_tiers or DEFAULT_CALIBRATION_FEATURE_TIERS)
    split_protocols = list(split_protocols or DEFAULT_SPLIT_PROTOCOLS)

    _log_event(
        events_path,
        "calibration_baselines_start",
        result_prefix=result_prefix,
        sample_per_file=sample_per_file,
        seed=seed,
        models=models,
        feature_tiers=feature_tiers,
        split_protocols=split_protocols,
    )

    audit = audit_csv_dir(csv_dir, work_dir / "audit")
    df = load_csvs(csv_dir, sample_per_file=sample_per_file, random_state=seed)
    data_hash = hash_dataframe(df)
    split_objects, skipped_splits = _build_splits(df, split_protocols, seed=seed)
    for skipped in skipped_splits:
        _log_event(events_path, "split_skipped", **skipped)

    rows: list[dict[str, Any]] = []
    for tier in feature_tiers:
        feature_info = select_feature_tier(df, tier)
        feature_hash = hash_object({"tier": tier, "columns": feature_info.columns})
        X_all, y_all, _ = make_xy(df, tier=tier, target="binary_label")

        for split in split_objects:
            X_train = X_all.loc[split.train_idx]
            y_train = y_all.loc[split.train_idx]
            X_val = X_all.loc[split.val_idx]
            y_val = y_all.loc[split.val_idx]
            X_test = X_all.loc[split.test_idx]
            y_test = y_all.loc[split.test_idx]

            for model_name in models:
                base = {
                    "experiment": result_prefix,
                    "seed": seed,
                    "model": model_name,
                    "feature_tier": tier,
                    "split": split.name,
                    "sample_per_file": sample_per_file,
                    "data_hash": data_hash,
                    "feature_hash": feature_hash,
                    "split_hash": split.split_hash,
                    "n_train": len(X_train),
                    "n_val": len(X_val),
                    "n_test": len(X_test),
                    "n_features": len(feature_info.columns),
                }
                _log_event(events_path, "calibration_run_start", **base)
                try:
                    fit = fit_predict(model_name, X_train, y_train, X_test, seed=seed)
                    if fit.y_prob is None or not hasattr(fit.model, "predict_proba"):
                        raise ValueError(f"Model {model_name} does not expose binary probabilities")

                    val_start = time.perf_counter()
                    val_prob = fit.model.predict_proba(X_val)[:, 1]
                    val_inference_seconds = time.perf_counter() - val_start
                    run_base = {
                        **base,
                        "status": "completed",
                        "train_seconds": fit.train_seconds,
                        "test_inference_seconds": fit.inference_seconds,
                        "val_inference_seconds": val_inference_seconds,
                        "warning_count": fit.warning_count,
                        "convergence_warning_count": fit.convergence_warning_count,
                    }
                    rows.append(
                        _metric_row(
                            run_base,
                            calibration_method="raw",
                            y_test=y_test,
                            y_prob=fit.y_prob,
                            calibration_seconds=0.0,
                        )
                    )

                    if _has_two_classes(y_val):
                        platt_prob, platt_seconds = _platt_calibrate(
                            y_val, val_prob, fit.y_prob, seed
                        )
                        rows.append(
                            _metric_row(
                                run_base,
                                calibration_method="platt_sigmoid",
                                y_test=y_test,
                                y_prob=platt_prob,
                                calibration_seconds=platt_seconds,
                            )
                        )
                        isotonic_prob, isotonic_seconds = _isotonic_calibrate(
                            y_val, val_prob, fit.y_prob
                        )
                        rows.append(
                            _metric_row(
                                run_base,
                                calibration_method="isotonic",
                                y_test=y_test,
                                y_prob=isotonic_prob,
                                calibration_seconds=isotonic_seconds,
                            )
                        )
                    else:
                        rows.append(
                            {
                                **run_base,
                                "status": "skipped",
                                "calibration_method": "platt_sigmoid",
                                "error_message": "Validation split has fewer than two classes",
                            }
                        )
                        rows.append(
                            {
                                **run_base,
                                "status": "skipped",
                                "calibration_method": "isotonic",
                                "error_message": "Validation split has fewer than two classes",
                            }
                        )
                    _log_event(events_path, "calibration_run_completed", **run_base)
                except Exception as exc:
                    row = {
                        **base,
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    }
                    rows.append(row)
                    _log_event(events_path, "calibration_run_failed", **row)

    results_path = results_dir / f"{result_prefix}_results.csv"
    pd.DataFrame(rows).to_csv(results_path, index=False)
    summary = {
        "audit": {
            "num_files": audit["num_files"],
            "total_rows": audit["total_rows"],
            "data_hash": audit["data_hash"],
        },
        "sample_rows": len(df),
        "seed": seed,
        "models": models,
        "feature_tiers": feature_tiers,
        "split_protocols": split_protocols,
        "skipped_splits": skipped_splits,
        "results_path": str(results_path),
        "events_path": str(events_path),
        "rows": len(rows),
        "failed_rows": int(sum(row.get("status") == "failed" for row in rows)),
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    summary_path = results_dir / f"{result_prefix}_summary.json"
    save_json(summary, summary_path)
    _log_event(events_path, "calibration_baselines_completed", **summary)
    with open(summary_path, encoding="utf-8") as f:
        return json.load(f)

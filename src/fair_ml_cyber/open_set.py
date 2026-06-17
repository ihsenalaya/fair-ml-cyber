"""Open-set baseline experiments."""

from __future__ import annotations

import json
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.data import load_csvs
from fair_ml_cyber.experiment import _log_event
from fair_ml_cyber.features import make_xy, select_feature_tier
from fair_ml_cyber.hashing import hash_dataframe, hash_object
from fair_ml_cyber.metrics import save_json
from fair_ml_cyber.modeling import fit_predict, is_open_set_model
from fair_ml_cyber.splits import open_set_holdout_split


DEFAULT_OPEN_SET_MODELS = ["isolation_forest", "local_outlier_factor"]
DEFAULT_OPEN_SET_FEATURE_TIERS = ["deployment_safe"]
DEFAULT_UNKNOWN_FAMILIES = ["Web", "Botnet", "PortScan", "DDoS"]


def _safe_metric(func, y_true: np.ndarray, y_score: np.ndarray) -> float | None:
    try:
        return float(func(y_true, y_score))
    except ValueError:
        return None


def _unknown_score(
    model_name: str,
    y_prob: np.ndarray,
    y_pred: np.ndarray,
) -> tuple[np.ndarray, str]:
    if is_open_set_model(model_name):
        return np.asarray(y_prob, dtype=float), "anomaly_score"
    score = 1.0 - np.maximum(y_prob, 1.0 - y_prob)
    return np.asarray(score, dtype=float), "classifier_uncertainty"


def run_open_set_baselines(
    csv_dir: str | Path,
    work_dir: str | Path,
    *,
    sample_per_file: int | None = None,
    seed: int = 42,
    models: Sequence[str] | None = None,
    feature_tiers: Sequence[str] | None = None,
    unknown_families: Sequence[str] | None = None,
    result_prefix: str = "open_set_baselines",
) -> dict[str, Any]:
    work_dir = Path(work_dir)
    results_dir = work_dir / "open_set_results"
    results_dir.mkdir(parents=True, exist_ok=True)
    events_path = results_dir / f"{result_prefix}_events.jsonl"
    if events_path.exists():
        events_path.unlink()

    models = list(models or DEFAULT_OPEN_SET_MODELS)
    feature_tiers = list(feature_tiers or DEFAULT_OPEN_SET_FEATURE_TIERS)
    unknown_families = list(unknown_families or DEFAULT_UNKNOWN_FAMILIES)

    _log_event(
        events_path,
        "open_set_baselines_start",
        result_prefix=result_prefix,
        sample_per_file=sample_per_file,
        seed=seed,
        models=models,
        feature_tiers=feature_tiers,
        unknown_families=unknown_families,
    )

    audit = audit_csv_dir(csv_dir, work_dir / "audit")
    df = load_csvs(csv_dir, sample_per_file=sample_per_file, random_state=seed)
    data_hash = hash_dataframe(df)

    rows: list[dict[str, Any]] = []
    for tier in feature_tiers:
        feature_info = select_feature_tier(df, tier)
        feature_hash = hash_object({"tier": tier, "columns": feature_info.columns})
        X_binary, y_binary, _ = make_xy(df, tier=tier, target="binary_label")

        for unknown_family in unknown_families:
            try:
                split = open_set_holdout_split(df, unknown_family=unknown_family, seed=seed)
            except ValueError as exc:
                rows.append(
                    {
                        "experiment": result_prefix,
                        "seed": seed,
                        "feature_tier": tier,
                        "unknown_family": unknown_family,
                        "status": "skipped",
                        "error_message": str(exc),
                    }
                )
                continue

            X_train = X_binary.loc[split.train_idx]
            y_train = y_binary.loc[split.train_idx]
            X_test = X_binary.loc[split.test_idx]
            y_unknown = (
                df.loc[split.test_idx, "attack_family"].astype(str) == unknown_family
            ).astype(int)

            for model_name in models:
                base = {
                    "experiment": result_prefix,
                    "seed": seed,
                    "model": model_name,
                    "feature_tier": tier,
                    "unknown_family": unknown_family,
                    "split": split.name,
                    "sample_per_file": sample_per_file,
                    "data_hash": data_hash,
                    "feature_hash": feature_hash,
                    "split_hash": split.split_hash,
                    "n_train": len(X_train),
                    "n_test": len(X_test),
                    "n_features": len(feature_info.columns),
                    "unknown_support": int(y_unknown.sum()),
                }
                _log_event(events_path, "open_set_baseline_start", **base)
                try:
                    fit = fit_predict(model_name, X_train, y_train, X_test, seed=seed)
                    y_prob = fit.y_prob if fit.y_prob is not None else fit.y_pred.astype(float)
                    score, score_name = _unknown_score(model_name, y_prob, fit.y_pred)
                    threshold = float(np.quantile(score, 0.90))
                    review = score >= threshold
                    unknown_mask = y_unknown.to_numpy().astype(bool)

                    if is_open_set_model(model_name):
                        attack_pred = fit.y_pred.astype(int)
                    else:
                        attack_pred = (np.asarray(y_prob, dtype=float) >= 0.5).astype(int)

                    row = {
                        **base,
                        "status": "completed",
                        "train_seconds": fit.train_seconds,
                        "inference_seconds": fit.inference_seconds,
                        "warning_count": fit.warning_count,
                        "convergence_warning_count": fit.convergence_warning_count,
                        "score_name": score_name,
                        "unknown_auroc_score": _safe_metric(
                            roc_auc_score, y_unknown.to_numpy(), score
                        ),
                        "unknown_auprc_score": _safe_metric(
                            average_precision_score, y_unknown.to_numpy(), score
                        ),
                        "unknown_attack_recall_as_attack": float(attack_pred[unknown_mask].mean())
                        if unknown_mask.any()
                        else None,
                        "review_rate_at_p90_score": float(review.mean()),
                        "unknown_recall_at_p90_score": float(review[unknown_mask].mean())
                        if unknown_mask.any()
                        else None,
                    }
                    rows.append(row)
                    _log_event(events_path, "open_set_baseline_completed", **row)
                except Exception as exc:
                    row = {
                        **base,
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                    }
                    rows.append(row)
                    _log_event(events_path, "open_set_baseline_failed", **row)

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
        "unknown_families": unknown_families,
        "results_path": str(results_path),
        "events_path": str(events_path),
        "runs": len(rows),
        "completed_runs": int(sum(row.get("status") == "completed" for row in rows)),
        "failed_runs": int(sum(row.get("status") == "failed" for row in rows)),
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    summary_path = results_dir / f"{result_prefix}_summary.json"
    save_json(summary, summary_path)
    _log_event(events_path, "open_set_baselines_completed", **summary)
    with open(summary_path, encoding="utf-8") as f:
        return json.load(f)

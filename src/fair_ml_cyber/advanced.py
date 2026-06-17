"""Advanced article analyses for FAIR-ML-CYBER."""

from __future__ import annotations

import json
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import average_precision_score, f1_score, roc_auc_score

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.data import RARE_LABELS, load_csvs
from fair_ml_cyber.experiment import DEFAULT_FEATURE_TIERS, _build_splits, _log_event
from fair_ml_cyber.features import make_xy, select_feature_tier
from fair_ml_cyber.hashing import hash_dataframe, hash_object
from fair_ml_cyber.metrics import (
    binary_metrics,
    expected_calibration_error,
    multiclass_metrics,
    save_json,
)
from fair_ml_cyber.modeling import fit_predict
from fair_ml_cyber.splits import open_set_holdout_split


DEFAULT_ADVANCED_MODELS = ["logistic_regression", "hist_gradient_boosting"]
DEFAULT_ADVANCED_SPLITS = [
    "random_stratified",
    "temporal",
    "latest_day_holdout",
    "scenario_holdout_Web",
    "endpoint_pair_holdout",
]
DEFAULT_UNKNOWN_FAMILIES = ["Web", "Botnet", "PortScan", "DDoS"]


def _safe_metric(func, y_true, y_score) -> float | None:
    try:
        return float(func(y_true, y_score))
    except ValueError:
        return None


def _calibration_rows(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    *,
    n_bins: int = 10,
) -> list[dict[str, Any]]:
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    rows = []
    for bin_id, (lo, hi) in enumerate(zip(bins[:-1], bins[1:])):
        if bin_id == 0:
            mask = (y_prob >= lo) & (y_prob <= hi)
        else:
            mask = (y_prob > lo) & (y_prob <= hi)
        count = int(mask.sum())
        if count == 0:
            rows.append(
                {
                    "bin": bin_id,
                    "bin_lower": float(lo),
                    "bin_upper": float(hi),
                    "count": 0,
                    "confidence_mean": None,
                    "positive_rate": None,
                    "abs_gap": None,
                }
            )
            continue
        confidence = float(y_prob[mask].mean())
        positive_rate = float(y_true[mask].mean())
        rows.append(
            {
                "bin": bin_id,
                "bin_lower": float(lo),
                "bin_upper": float(hi),
                "count": count,
                "confidence_mean": confidence,
                "positive_rate": positive_rate,
                "abs_gap": abs(confidence - positive_rate),
            }
        )
    return rows


def _abstention_rows(y_true: np.ndarray, y_prob: np.ndarray) -> list[dict[str, Any]]:
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob).astype(float)
    confidence = np.maximum(y_prob, 1.0 - y_prob)
    rows = []
    for target_coverage in [1.0, 0.95, 0.90, 0.80, 0.70, 0.50]:
        threshold = float(np.quantile(confidence, 1.0 - target_coverage))
        accepted = confidence >= threshold
        accepted_count = int(accepted.sum())
        if accepted_count == 0:
            rows.append(
                {
                    "target_coverage": target_coverage,
                    "actual_coverage": 0.0,
                    "review_rate": 1.0,
                    "confidence_threshold": threshold,
                    "selective_error": None,
                    "selective_macro_f1": None,
                    "accepted_attack_recall": None,
                }
            )
            continue
        y_pred = (y_prob[accepted] >= 0.5).astype(int)
        y_acc = y_true[accepted]
        selective_error = float((y_pred != y_acc).mean())
        attack_mask = y_acc == 1
        accepted_attack_recall = None
        if attack_mask.any():
            accepted_attack_recall = float((y_pred[attack_mask] == 1).mean())
        rows.append(
            {
                "target_coverage": target_coverage,
                "actual_coverage": float(accepted.mean()),
                "review_rate": float(1.0 - accepted.mean()),
                "confidence_threshold": threshold,
                "selective_error": selective_error,
                "selective_macro_f1": float(f1_score(y_acc, y_pred, average="macro", zero_division=0)),
                "accepted_attack_recall": accepted_attack_recall,
            }
        )
    return rows


def _coefficient_importance(model: Any, columns: list[str]) -> pd.DataFrame | None:
    if not hasattr(model, "named_steps") or "model" not in model.named_steps:
        return None
    estimator = model.named_steps["model"]
    if not hasattr(estimator, "coef_"):
        return None
    coef = np.asarray(estimator.coef_)
    if coef.ndim == 1:
        importance = np.abs(coef)
    else:
        importance = np.abs(coef).mean(axis=0)
    return pd.DataFrame({"feature": columns, "importance": importance.astype(float)})


def _permutation_importance_frame(
    model: Any,
    X: pd.DataFrame,
    y: pd.Series,
    *,
    seed: int,
    sample_size: int,
    n_repeats: int,
) -> pd.DataFrame:
    if len(X) > sample_size:
        sample_idx = X.sample(n=sample_size, random_state=seed).index
        X_eval = X.loc[sample_idx]
        y_eval = y.loc[sample_idx]
    else:
        X_eval = X
        y_eval = y
    result = permutation_importance(
        model,
        X_eval,
        y_eval,
        n_repeats=n_repeats,
        random_state=seed,
        scoring="f1_macro",
        n_jobs=1,
    )
    return pd.DataFrame(
        {
            "feature": list(X.columns),
            "importance": result.importances_mean.astype(float),
            "importance_std": result.importances_std.astype(float),
            "explain_sample_size": len(X_eval),
            "permutation_repeats": n_repeats,
        }
    )


def _topk_stability(importance_df: pd.DataFrame, *, top_k: int = 15) -> pd.DataFrame:
    rows = []
    if importance_df.empty:
        return pd.DataFrame(rows)
    group_cols = ["task", "model", "feature_tier", "seed"]
    for group_key, group in importance_df.groupby(group_cols):
        task, model, tier, seed = group_key
        by_split = {}
        for split, split_df in group.groupby("split"):
            ordered = split_df.sort_values("importance", ascending=False)
            by_split[split] = set(ordered.head(top_k)["feature"].astype(str))
        baseline = by_split.get("random_stratified")
        if not baseline:
            continue
        for split, features in by_split.items():
            if split == "random_stratified":
                continue
            union = baseline | features
            rows.append(
                {
                    "task": task,
                    "model": model,
                    "feature_tier": tier,
                    "seed": seed,
                    "baseline_split": "random_stratified",
                    "target_split": split,
                    "top_k": top_k,
                    "jaccard": float(len(baseline & features) / len(union)) if union else None,
                    "overlap_count": int(len(baseline & features)),
                }
            )
    return pd.DataFrame(rows)


def run_advanced_analysis(
    csv_dir: str | Path,
    work_dir: str | Path,
    *,
    sample_per_file: int | None = None,
    seed: int = 42,
    models: Sequence[str] | None = None,
    feature_tiers: Sequence[str] | None = None,
    split_protocols: Sequence[str] | None = None,
    unknown_families: Sequence[str] | None = None,
    result_prefix: str = "advanced",
    explain_sample_size: int = 5000,
    permutation_repeats: int = 2,
) -> dict[str, Any]:
    work_dir = Path(work_dir)
    results_dir = work_dir / "advanced_results"
    results_dir.mkdir(parents=True, exist_ok=True)
    events_path = results_dir / f"{result_prefix}_events.jsonl"
    if events_path.exists():
        events_path.unlink()

    models = list(models or DEFAULT_ADVANCED_MODELS)
    feature_tiers = list(feature_tiers or DEFAULT_FEATURE_TIERS)
    split_protocols = list(split_protocols or DEFAULT_ADVANCED_SPLITS)
    unknown_families = list(unknown_families or DEFAULT_UNKNOWN_FAMILIES)

    _log_event(
        events_path,
        "advanced_start",
        result_prefix=result_prefix,
        sample_per_file=sample_per_file,
        seed=seed,
        models=models,
        feature_tiers=feature_tiers,
        split_protocols=split_protocols,
        unknown_families=unknown_families,
    )

    audit = audit_csv_dir(csv_dir, work_dir / "audit")
    df = load_csvs(csv_dir, sample_per_file=sample_per_file, random_state=seed)
    data_hash = hash_dataframe(df)
    split_objects, skipped_splits = _build_splits(df, split_protocols, seed=seed)

    binary_rows: list[dict[str, Any]] = []
    calibration_rows: list[dict[str, Any]] = []
    abstention_rows: list[dict[str, Any]] = []
    multiclass_rows: list[dict[str, Any]] = []
    per_class_rows: list[dict[str, Any]] = []
    rare_rows: list[dict[str, Any]] = []
    open_set_rows: list[dict[str, Any]] = []
    importance_rows: list[pd.DataFrame] = []

    for tier in feature_tiers:
        feature_info = select_feature_tier(df, tier)
        feature_hash = hash_object({"tier": tier, "columns": feature_info.columns})
        X_binary, y_binary, _ = make_xy(df, tier=tier, target="binary_label")
        X_multi, y_multi, _ = make_xy(df, tier=tier, target="label")

        for split in split_objects:
            X_train_binary = X_binary.loc[split.train_idx]
            y_train_binary = y_binary.loc[split.train_idx]
            X_test_binary = X_binary.loc[split.test_idx]
            y_test_binary = y_binary.loc[split.test_idx]
            X_train_multi = X_multi.loc[split.train_idx]
            y_train_multi = y_multi.loc[split.train_idx]
            X_test_multi = X_multi.loc[split.test_idx]
            y_test_multi = y_multi.loc[split.test_idx]

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
                    "n_train": len(X_train_binary),
                    "n_test": len(X_test_binary),
                    "n_features": len(feature_info.columns),
                }

                _log_event(events_path, "binary_run_start", **base)
                fit = fit_predict(model_name, X_train_binary, y_train_binary, X_test_binary, seed=seed)
                y_prob = fit.y_prob if fit.y_prob is not None else fit.y_pred.astype(float)
                metrics = binary_metrics(y_test_binary.to_numpy(), y_prob)
                binary_rows.append(
                    {
                        **base,
                        "task": "binary",
                        "train_seconds": fit.train_seconds,
                        "inference_seconds": fit.inference_seconds,
                        "warning_count": fit.warning_count,
                        "convergence_warning_count": fit.convergence_warning_count,
                        **metrics,
                    }
                )
                for row in _calibration_rows(y_test_binary.to_numpy(), y_prob):
                    calibration_rows.append({**base, **row})
                for row in _abstention_rows(y_test_binary.to_numpy(), y_prob):
                    abstention_rows.append({**base, **row})

                coef_imp = _coefficient_importance(fit.model, feature_info.columns)
                if coef_imp is None:
                    coef_imp = _permutation_importance_frame(
                        fit.model,
                        X_test_binary,
                        y_test_binary,
                        seed=seed,
                        sample_size=explain_sample_size,
                        n_repeats=permutation_repeats,
                    )
                    method = "permutation"
                else:
                    method = "coefficient"
                    coef_imp["importance_std"] = None
                    coef_imp["explain_sample_size"] = len(X_test_binary)
                    coef_imp["permutation_repeats"] = 0
                coef_imp = coef_imp.assign(task="binary", method=method, **base)
                importance_rows.append(coef_imp)

                _log_event(
                    events_path,
                    "binary_run_completed",
                    **base,
                    macro_f1=metrics.get("macro_f1"),
                    ece=metrics.get("ece"),
                    convergence_warning_count=fit.convergence_warning_count,
                )

                _log_event(events_path, "multiclass_run_start", **base)
                multi_fit = fit_predict(model_name, X_train_multi, y_train_multi, X_test_multi, seed=seed)
                multi_metrics = multiclass_metrics(y_test_multi.to_numpy(), multi_fit.y_pred)
                multiclass_rows.append(
                    {
                        **base,
                        "task": "multiclass_label",
                        "train_seconds": multi_fit.train_seconds,
                        "inference_seconds": multi_fit.inference_seconds,
                        "warning_count": multi_fit.warning_count,
                        "convergence_warning_count": multi_fit.convergence_warning_count,
                        "macro_f1": multi_metrics["macro_f1"],
                        "weighted_f1": multi_metrics["weighted_f1"],
                        "balanced_accuracy": multi_metrics["balanced_accuracy"],
                        "mcc": multi_metrics["mcc"],
                        "num_labels": len(multi_metrics["labels"]),
                    }
                )
                for label, values in multi_metrics["per_class"].items():
                    row = {**base, "label": label, **values}
                    per_class_rows.append(row)
                    if label in RARE_LABELS:
                        rare_rows.append(row)
                _log_event(
                    events_path,
                    "multiclass_run_completed",
                    **base,
                    macro_f1=multi_metrics["macro_f1"],
                    convergence_warning_count=multi_fit.convergence_warning_count,
                )

        for unknown_family in unknown_families:
            try:
                split = open_set_holdout_split(df, unknown_family=unknown_family, seed=seed)
            except ValueError as exc:
                open_set_rows.append(
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
            y_unknown = (df.loc[split.test_idx, "attack_family"].astype(str) == unknown_family).astype(int)
            for model_name in models:
                base = {
                    "experiment": result_prefix,
                    "seed": seed,
                    "model": model_name,
                    "feature_tier": tier,
                    "unknown_family": unknown_family,
                    "split": split.name,
                    "data_hash": data_hash,
                    "feature_hash": feature_hash,
                    "split_hash": split.split_hash,
                    "n_train": len(X_train),
                    "n_test": len(X_test),
                    "unknown_support": int(y_unknown.sum()),
                }
                _log_event(events_path, "open_set_run_start", **base)
                fit = fit_predict(model_name, X_train, y_train, X_test, seed=seed)
                attack_prob = fit.y_prob if fit.y_prob is not None else fit.y_pred.astype(float)
                uncertainty = 1.0 - np.maximum(attack_prob, 1.0 - attack_prob)
                threshold = float(np.quantile(uncertainty, 0.90))
                review = uncertainty >= threshold
                open_set_rows.append(
                    {
                        **base,
                        "status": "completed",
                        "train_seconds": fit.train_seconds,
                        "inference_seconds": fit.inference_seconds,
                        "warning_count": fit.warning_count,
                        "convergence_warning_count": fit.convergence_warning_count,
                        "unknown_auroc_uncertainty": _safe_metric(roc_auc_score, y_unknown, uncertainty),
                        "unknown_auprc_uncertainty": _safe_metric(
                            average_precision_score, y_unknown, uncertainty
                        ),
                        "unknown_attack_recall_as_attack": float(
                            ((attack_prob[y_unknown == 1] >= 0.5).astype(int) == 1).mean()
                        )
                        if int(y_unknown.sum()) > 0
                        else None,
                        "review_rate_at_p90_uncertainty": float(review.mean()),
                        "unknown_recall_at_p90_uncertainty": float(review[y_unknown == 1].mean())
                        if int(y_unknown.sum()) > 0
                        else None,
                    }
                )
                _log_event(events_path, "open_set_run_completed", **base)

    importance_df = pd.concat(importance_rows, ignore_index=True) if importance_rows else pd.DataFrame()
    stability_df = _topk_stability(importance_df, top_k=15)

    outputs = {
        "binary_results": results_dir / f"{result_prefix}_binary_results.csv",
        "calibration_bins": results_dir / f"{result_prefix}_calibration_bins.csv",
        "abstention_curves": results_dir / f"{result_prefix}_abstention_curves.csv",
        "multiclass_results": results_dir / f"{result_prefix}_multiclass_results.csv",
        "per_class_results": results_dir / f"{result_prefix}_per_class_results.csv",
        "rare_class_results": results_dir / f"{result_prefix}_rare_class_results.csv",
        "open_set_results": results_dir / f"{result_prefix}_open_set_results.csv",
        "feature_importance": results_dir / f"{result_prefix}_feature_importance.csv",
        "explanation_stability": results_dir / f"{result_prefix}_explanation_stability.csv",
    }

    pd.DataFrame(binary_rows).to_csv(outputs["binary_results"], index=False)
    pd.DataFrame(calibration_rows).to_csv(outputs["calibration_bins"], index=False)
    pd.DataFrame(abstention_rows).to_csv(outputs["abstention_curves"], index=False)
    pd.DataFrame(multiclass_rows).to_csv(outputs["multiclass_results"], index=False)
    pd.DataFrame(per_class_rows).to_csv(outputs["per_class_results"], index=False)
    pd.DataFrame(rare_rows).to_csv(outputs["rare_class_results"], index=False)
    pd.DataFrame(open_set_rows).to_csv(outputs["open_set_results"], index=False)
    importance_df.to_csv(outputs["feature_importance"], index=False)
    stability_df.to_csv(outputs["explanation_stability"], index=False)

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
        "unknown_families": unknown_families,
        "skipped_splits": skipped_splits,
        "outputs": {k: str(v) for k, v in outputs.items()},
        "binary_runs": len(binary_rows),
        "multiclass_runs": len(multiclass_rows),
        "open_set_runs": len(open_set_rows),
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    summary_path = results_dir / f"{result_prefix}_summary.json"
    save_json(summary, summary_path)
    _log_event(events_path, "advanced_completed", **summary)
    return summary

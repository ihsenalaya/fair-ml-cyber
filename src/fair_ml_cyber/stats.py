"""Robust summary statistics for completed experiment result tables."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


def _clean_group_cols(df: pd.DataFrame, cols: Iterable[str]) -> list[str]:
    return [col for col in cols if col in df.columns]


def _completed_rows(df: pd.DataFrame) -> pd.DataFrame:
    if "status" not in df.columns:
        return df.copy()
    return df[df["status"].astype(str).str.lower() == "completed"].copy()


def load_result_tables(paths: Iterable[str | Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        path = Path(path)
        frame = pd.read_csv(path)
        frame["result_source"] = str(path)
        frames.append(frame)
    if not frames:
        raise ValueError("At least one result CSV is required")
    return pd.concat(frames, ignore_index=True, sort=False)


def bootstrap_ci(
    values: Iterable[float],
    *,
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict[str, float | int | None]:
    arr = pd.Series(list(values), dtype="float64").dropna().to_numpy()
    n = int(arr.size)
    if n == 0:
        return {"n": 0, "mean": None, "std": None, "ci_low": None, "ci_high": None}
    mean = float(np.mean(arr))
    std = float(np.std(arr, ddof=1)) if n > 1 else 0.0
    if n == 1 or n_boot <= 0:
        return {"n": n, "mean": mean, "std": std, "ci_low": mean, "ci_high": mean}

    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, n, size=(n_boot, n))
    boot_means = arr[sample_idx].mean(axis=1)
    alpha = (1.0 - confidence) / 2.0
    return {
        "n": n,
        "mean": mean,
        "std": std,
        "ci_low": float(np.quantile(boot_means, alpha)),
        "ci_high": float(np.quantile(boot_means, 1.0 - alpha)),
    }


def summarize_metric(
    df: pd.DataFrame,
    *,
    metric: str = "macro_f1",
    group_cols: Iterable[str] = ("model", "split"),
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> pd.DataFrame:
    if metric not in df.columns:
        raise ValueError(f"Metric column not found: {metric}")
    clean = _completed_rows(df)
    clean[metric] = pd.to_numeric(clean[metric], errors="coerce")
    groups = _clean_group_cols(clean, group_cols)
    rows: list[dict[str, Any]] = []
    grouped = clean.groupby(groups, dropna=False) if groups else [((), clean)]
    for key, group in grouped:
        if not isinstance(key, tuple):
            key = (key,)
        stats = bootstrap_ci(
            group[metric],
            n_boot=n_boot,
            confidence=confidence,
            seed=seed,
        )
        row = dict(zip(groups, key))
        row.update(
            {
                "metric": metric,
                "confidence": confidence,
                "bootstrap_iterations": n_boot,
                **stats,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def _sign_flip_p_value(diffs: np.ndarray) -> float | None:
    diffs = np.asarray(diffs, dtype=float)
    diffs = diffs[np.isfinite(diffs)]
    n = diffs.size
    if n == 0 or np.allclose(diffs, 0.0):
        return None
    observed = abs(float(np.mean(diffs)))
    if n <= 20:
        extreme = 0
        total = 0
        for signs in itertools.product((-1.0, 1.0), repeat=n):
            total += 1
            mean = abs(float(np.mean(diffs * np.asarray(signs))))
            if mean >= observed - 1e-12:
                extreme += 1
        return float(extreme / total)

    rng = np.random.default_rng(42)
    signs = rng.choice([-1.0, 1.0], size=(20000, n))
    means = np.abs((signs * diffs).mean(axis=1))
    return float(np.mean(means >= observed - 1e-12))


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"

    def fmt(value: Any) -> str:
        if pd.isna(value):
            return ""
        if isinstance(value, float):
            return f"{value:.6g}"
        return str(value).replace("|", "\\|")

    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(fmt(row[col]) for col in columns) + " |")
    return "\n".join(lines)


def paired_split_comparisons(
    df: pd.DataFrame,
    *,
    metric: str = "macro_f1",
    random_split: str = "random_stratified",
    group_cols: Iterable[str] = ("model",),
    pair_cols: Iterable[str] = ("seed", "feature_tier"),
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> pd.DataFrame:
    if metric not in df.columns:
        raise ValueError(f"Metric column not found: {metric}")
    if "split" not in df.columns:
        raise ValueError("Column 'split' is required for paired split comparisons")

    clean = _completed_rows(df)
    clean[metric] = pd.to_numeric(clean[metric], errors="coerce")
    groups = _clean_group_cols(clean, group_cols)
    pairs = _clean_group_cols(clean, pair_cols)
    if not pairs:
        raise ValueError("At least one available pair column is required")

    index_cols = groups + pairs
    pivot = clean.pivot_table(
        index=index_cols,
        columns="split",
        values=metric,
        aggfunc="mean",
    ).reset_index()
    if random_split not in pivot.columns:
        raise ValueError(f"Random split not present: {random_split}")

    stress_splits = sorted(
        split for split in clean["split"].dropna().unique().tolist() if split != random_split
    )
    rows: list[dict[str, Any]] = []
    grouped = pivot.groupby(groups, dropna=False) if groups else [((), pivot)]
    for key, group in grouped:
        if not isinstance(key, tuple):
            key = (key,)
        key_values = dict(zip(groups, key))
        for stress_split in stress_splits:
            if stress_split not in group.columns:
                continue
            paired = group[[random_split, stress_split]].dropna()
            if paired.empty:
                continue
            baseline = paired[random_split].astype(float).to_numpy()
            stress = paired[stress_split].astype(float).to_numpy()
            diffs = stress - baseline
            ratios = np.divide(
                stress,
                baseline,
                out=np.full_like(stress, np.nan, dtype=float),
                where=baseline != 0,
            )
            diff_stats = bootstrap_ci(
                diffs,
                n_boot=n_boot,
                confidence=confidence,
                seed=seed,
            )
            ratio_stats = bootstrap_ci(
                ratios,
                n_boot=n_boot,
                confidence=confidence,
                seed=seed + 1,
            )
            diff_std = float(np.std(diffs, ddof=1)) if diffs.size > 1 else 0.0
            effect_size = float(np.mean(diffs) / diff_std) if diff_std > 0 else None
            row = {
                **key_values,
                "metric": metric,
                "baseline_split": random_split,
                "stress_split": stress_split,
                "n_pairs": int(paired.shape[0]),
                "baseline_mean": float(np.mean(baseline)),
                "stress_mean": float(np.mean(stress)),
                "mean_delta": diff_stats["mean"],
                "delta_ci_low": diff_stats["ci_low"],
                "delta_ci_high": diff_stats["ci_high"],
                "mean_ratio": ratio_stats["mean"],
                "ratio_ci_low": ratio_stats["ci_low"],
                "ratio_ci_high": ratio_stats["ci_high"],
                "paired_effect_size_dz": effect_size,
                "sign_flip_p_value": _sign_flip_p_value(diffs),
                "confidence": confidence,
                "bootstrap_iterations": n_boot,
            }
            rows.append(row)
    return pd.DataFrame(rows)


def inter_seed_variance(
    df: pd.DataFrame,
    *,
    metric: str = "macro_f1",
    group_cols: Iterable[str] = ("model", "feature_tier", "split"),
) -> pd.DataFrame:
    if metric not in df.columns:
        raise ValueError(f"Metric column not found: {metric}")
    if "seed" not in df.columns:
        raise ValueError("Column 'seed' is required for inter-seed variance")

    clean = _completed_rows(df)
    clean[metric] = pd.to_numeric(clean[metric], errors="coerce")
    groups = _clean_group_cols(clean, group_cols)
    per_seed = clean.groupby(groups + ["seed"], dropna=False)[metric].mean().reset_index()
    rows: list[dict[str, Any]] = []
    grouped = per_seed.groupby(groups, dropna=False) if groups else [((), per_seed)]
    for key, group in grouped:
        if not isinstance(key, tuple):
            key = (key,)
        values = group[metric].dropna().astype(float)
        row = dict(zip(groups, key))
        row.update(
            {
                "metric": metric,
                "n_seeds": int(values.shape[0]),
                "mean_across_seeds": float(values.mean()) if not values.empty else None,
                "inter_seed_std": float(values.std(ddof=1)) if values.shape[0] > 1 else 0.0,
                "inter_seed_variance": float(values.var(ddof=1)) if values.shape[0] > 1 else 0.0,
                "min_seed_metric": float(values.min()) if not values.empty else None,
                "max_seed_metric": float(values.max()) if not values.empty else None,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def _write_markdown_report(
    output_path: Path,
    *,
    result_paths: list[str],
    metric: str,
    summary: pd.DataFrame,
    comparisons: pd.DataFrame,
    seed_variance: pd.DataFrame,
) -> None:
    lines = [
        "# Q1 Robust Statistics Snapshot",
        "",
        "This report is generated from verified result CSV files. Bootstrap intervals are over",
        "available experimental units, not over individual flow-level predictions.",
        "",
        "## Inputs",
        "",
    ]
    lines.extend(f"- `{path}`" for path in result_paths)
    lines.extend(["", f"Metric: `{metric}`", ""])

    if not comparisons.empty:
        cols = [
            col
            for col in [
                "model",
                "stress_split",
                "n_pairs",
                "baseline_mean",
                "stress_mean",
                "mean_delta",
                "delta_ci_low",
                "delta_ci_high",
                "mean_ratio",
                "ratio_ci_low",
                "ratio_ci_high",
                "paired_effect_size_dz",
                "sign_flip_p_value",
            ]
            if col in comparisons.columns
        ]
        lines.extend(["## Random vs Stress Paired Comparisons", ""])
        lines.append(_markdown_table(comparisons[cols].round(6)))
        lines.append("")

    if not seed_variance.empty:
        cols = [
            col
            for col in [
                "model",
                "feature_tier",
                "split",
                "n_seeds",
                "mean_across_seeds",
                "inter_seed_std",
                "min_seed_metric",
                "max_seed_metric",
            ]
            if col in seed_variance.columns
        ]
        lines.extend(["## Inter-Seed Variance", ""])
        lines.append(_markdown_table(seed_variance[cols].round(6)))
        lines.append("")

    if not summary.empty:
        lines.extend(["## Bootstrap Metric Summary", ""])
        shown = summary.head(40).round(6)
        lines.append(_markdown_table(shown))
        if summary.shape[0] > shown.shape[0]:
            lines.append("")
            lines.append(f"Only the first {shown.shape[0]} rows are shown in this Markdown report.")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_q1_statistics(
    result_paths: Iterable[str | Path],
    output_dir: str | Path,
    *,
    metric: str = "macro_f1",
    n_boot: int = 2000,
    confidence: float = 0.95,
    seed: int = 42,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_paths = [str(Path(path)) for path in result_paths]
    df = load_result_tables(result_paths)

    summary = summarize_metric(
        df,
        metric=metric,
        group_cols=("model", "feature_tier", "split"),
        n_boot=n_boot,
        confidence=confidence,
        seed=seed,
    )
    comparisons = paired_split_comparisons(
        df,
        metric=metric,
        random_split="random_stratified",
        group_cols=("model",),
        pair_cols=("seed", "feature_tier"),
        n_boot=n_boot,
        confidence=confidence,
        seed=seed,
    )
    seed_variance = inter_seed_variance(
        df,
        metric=metric,
        group_cols=("model", "feature_tier", "split"),
    )

    summary_path = output_dir / "q1_metric_summary.csv"
    comparisons_path = output_dir / "q1_paired_split_comparisons.csv"
    variance_path = output_dir / "q1_inter_seed_variance.csv"
    report_path = output_dir / "q1_statistics_report.md"
    metadata_path = output_dir / "q1_statistics_summary.json"

    summary.to_csv(summary_path, index=False)
    comparisons.to_csv(comparisons_path, index=False)
    seed_variance.to_csv(variance_path, index=False)
    _write_markdown_report(
        report_path,
        result_paths=result_paths,
        metric=metric,
        summary=summary,
        comparisons=comparisons,
        seed_variance=seed_variance,
    )

    metadata = {
        "metric": metric,
        "confidence": confidence,
        "bootstrap_iterations": n_boot,
        "seed": seed,
        "input_result_paths": result_paths,
        "input_rows": int(df.shape[0]),
        "completed_rows": int(_completed_rows(df).shape[0]),
        "outputs": {
            "metric_summary": str(summary_path),
            "paired_split_comparisons": str(comparisons_path),
            "inter_seed_variance": str(variance_path),
            "report": str(report_path),
            "summary": str(metadata_path),
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata

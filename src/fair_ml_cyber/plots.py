"""Publication-oriented figures generated from real outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_label_distribution(labels_csv: str | Path, output_path: str | Path) -> None:
    df = pd.read_csv(labels_csv)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["label"], df["rows"])
    ax.set_yscale("log")
    ax.set_ylabel("Flows (log scale)")
    ax.set_xlabel("Label")
    ax.tick_params(axis="x", rotation=60)
    ax.set_title("Label distribution")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_metric_by_split(results_csv: str | Path, output_path: str | Path, metric: str = "macro_f1") -> None:
    df = pd.read_csv(results_csv)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pivot = df.pivot_table(index="split", columns="model", values=metric, aggfunc="mean")
    fig, ax = plt.subplots(figsize=(9, 5))
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} by split and model")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_split_gap(
    results_csvs: list[str | Path],
    output_path: str | Path,
    metric: str = "macro_f1",
) -> dict[str, str]:
    frames = []
    for path in results_csvs:
        frame = pd.read_csv(path)
        frame["result_source"] = str(path)
        frames.append(frame)
    if not frames:
        raise ValueError("At least one result CSV is required")

    df = pd.concat(frames, ignore_index=True, sort=False)
    if "status" in df.columns:
        df = df[df["status"].astype(str).str.lower() == "completed"].copy()
    if metric not in df.columns:
        raise ValueError(f"Metric column not found: {metric}")
    df[metric] = pd.to_numeric(df[metric], errors="coerce")

    split_order = [
        "random_stratified",
        "temporal",
        "day_holdout_2017-07-07",
        "scenario_holdout_Web",
        "endpoint_pair_holdout",
    ]
    split_labels = {
        "random_stratified": "Random",
        "temporal": "Temporal",
        "day_holdout_2017-07-07": "Latest day",
        "scenario_holdout_Web": "Web holdout",
        "endpoint_pair_holdout": "Endpoint-pair",
    }
    model_labels = {
        "hist_gradient_boosting": "HGB",
        "logistic_regression": "LR",
        "random_forest": "RF",
    }

    summary = (
        df.groupby(["split", "model"], dropna=False)[metric]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    summary["split"] = pd.Categorical(summary["split"], categories=split_order, ordered=True)
    summary = summary.sort_values(["split", "model"])
    pivot_mean = summary.pivot(index="split", columns="model", values="mean").dropna(how="all")
    pivot_std = summary.pivot(index="split", columns="model", values="std").reindex_like(pivot_mean)
    pivot_mean.index = [split_labels.get(str(idx), str(idx)) for idx in pivot_mean.index]
    pivot_std.index = pivot_mean.index
    pivot_mean = pivot_mean.rename(columns=model_labels)
    pivot_std = pivot_std.rename(columns=model_labels)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    pivot_mean.plot(
        kind="bar",
        ax=ax,
        yerr=pivot_std.fillna(0.0),
        capsize=3,
        width=0.78,
        color=["#2f6fbb", "#d9792b", "#4b8b3b"][: len(pivot_mean.columns)],
    )
    ax.set_ylim(0.0, 1.05)
    ax.set_ylabel(metric.replace("_", "-"))
    ax.set_xlabel("")
    ax.set_title("Random split overstates deployment-oriented performance")
    ax.legend(title="Model", loc="upper right", frameon=False)
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.25, linewidth=0.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return {"figure_path": str(output_path)}


def plot_per_class_heatmap(
    per_class_csv: str | Path,
    output_path: str | Path,
    *,
    model: str = "hist_gradient_boosting",
    metric: str = "f1",
    min_support: int = 1,
) -> dict[str, str]:
    df = pd.read_csv(per_class_csv)
    required = {"model", "split", "label", metric, "support"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df = df[df["model"].astype(str) == model].copy()
    if df.empty:
        raise ValueError(f"No rows found for model: {model}")
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
    df["support"] = pd.to_numeric(df["support"], errors="coerce").fillna(0).astype(int)

    support_by_label = df.groupby("label")["support"].max()
    kept_labels = support_by_label[support_by_label >= min_support].sort_values(ascending=False).index
    df = df[df["label"].isin(kept_labels)].copy()

    split_order = [
        "random_stratified",
        "temporal",
        "day_holdout_2017-07-07",
        "scenario_holdout_Web",
        "endpoint_pair_holdout",
    ]
    split_labels = {
        "random_stratified": "Random",
        "temporal": "Temporal",
        "day_holdout_2017-07-07": "Latest day",
        "scenario_holdout_Web": "Web holdout",
        "endpoint_pair_holdout": "Endpoint-pair",
    }
    pivot = df.pivot_table(index="label", columns="split", values=metric, aggfunc="mean")
    pivot = pivot.reindex(index=kept_labels, columns=split_order)
    display_columns = [split_labels.get(str(col), str(col)) for col in pivot.columns]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    height = max(4.8, 0.34 * len(pivot.index))
    fig, ax = plt.subplots(figsize=(8.8, height))
    cmap = plt.cm.viridis.copy()
    cmap.set_bad("#d9d9d9")
    values = np.ma.masked_invalid(pivot.to_numpy(dtype=float))
    image = ax.imshow(values, aspect="auto", vmin=0.0, vmax=1.0, cmap=cmap)
    ax.set_xticks(range(len(display_columns)))
    ax.set_xticklabels(display_columns, rotation=25, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([str(label).replace("_", " ") for label in pivot.index], fontsize=8)
    ax.set_title(f"Per-class {metric.upper()} under split protocols ({model.replace('_', ' ')})")
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label(metric.upper())
    ax.set_xlabel("Split protocol")
    ax.set_ylabel("Class label")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220)
    plt.close(fig)
    return {"figure_path": str(output_path)}

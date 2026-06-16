"""Publication-oriented figures generated from real outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
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


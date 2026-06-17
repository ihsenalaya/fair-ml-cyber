"""Dataset sampling utilities for large external CSV collections."""

from __future__ import annotations

from pathlib import Path
from zlib import adler32

import numpy as np
import pandas as pd

from fair_ml_cyber.data import canonicalize_column_name


def _label_cap(label: str, benign_cap: int, attack_cap: int) -> int:
    return benign_cap if str(label).strip().lower() == "benign" else attack_cap


def build_stratified_sample(
    csv_dir: str | Path,
    output_dir: str | Path,
    *,
    benign_cap: int = 80_000,
    attack_cap: int = 30_000,
    seed: int = 42,
    result_name: str = "stratified_sample.csv",
    chunksize: int = 100_000,
) -> dict:
    """Create a real-data label-stratified sample from large CSV files."""
    csv_dir = Path(csv_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / result_name

    reservoirs: dict[str, pd.DataFrame] = {}
    seen_counts: dict[str, int] = {}
    for path in sorted(csv_dir.glob("*.csv")):
        file_seed = seed + adler32(path.name.encode("utf-8"))
        rng = np.random.default_rng(file_seed)
        for chunk in pd.read_csv(path, chunksize=chunksize, dtype=str):
            chunk = chunk.copy()
            chunk.columns = [canonicalize_column_name(c) for c in chunk.columns]
            if "label" not in chunk.columns:
                raise ValueError(f"Expected label column in {path}")
            chunk["label"] = chunk["label"].astype(str).str.strip()
            chunk = chunk[chunk["label"].str.lower() != "label"].copy()
            if chunk.empty:
                continue
            chunk["source_file_original"] = path.name
            chunk["_sample_key"] = rng.random(len(chunk))
            for label, group in chunk.groupby("label", sort=False):
                seen_counts[label] = seen_counts.get(label, 0) + len(group)
                if label in reservoirs:
                    candidate = pd.concat([reservoirs[label], group], ignore_index=True)
                else:
                    candidate = group
                reservoirs[label] = candidate.nsmallest(
                    _label_cap(label, benign_cap, attack_cap), "_sample_key"
                )

    if not reservoirs:
        raise FileNotFoundError(f"No CSV rows sampled from {csv_dir}")

    sample = pd.concat(reservoirs.values(), ignore_index=True)
    sample = sample.drop(columns=["_sample_key"])
    sample = sample.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    sample.to_csv(output_path, index=False)

    sampled_counts = sample["label"].value_counts().sort_index().to_dict()
    summary = {
        "csv_dir": str(csv_dir),
        "output_path": str(output_path),
        "rows": int(len(sample)),
        "seen_label_counts": {k: int(v) for k, v in sorted(seen_counts.items())},
        "sampled_label_counts": {k: int(v) for k, v in sampled_counts.items()},
        "benign_cap": benign_cap,
        "attack_cap": attack_cap,
        "seed": seed,
    }
    summary_path = output_dir / f"{Path(result_name).stem}_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        import json

        json.dump(summary, f, indent=2)
    summary["summary_path"] = str(summary_path)
    return summary

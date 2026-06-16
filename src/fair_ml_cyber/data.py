"""Data loading and preprocessing."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


RARE_LABELS = {"Heartbleed", "Web_SQL_Injection", "Web_XSS", "Web_Brute_Force"}


def attack_family(label: str) -> str:
    if label == "Benign":
        return "Benign"
    if label.startswith("DoS_"):
        return "DoS"
    if label.startswith("DDoS"):
        return "DDoS"
    if label.startswith("Web_"):
        return "Web"
    if "Patator" in label:
        return "BruteForce"
    if label.startswith("Port"):
        return "PortScan"
    if label.startswith("Botnet"):
        return "Botnet"
    if label == "Heartbleed":
        return "Heartbleed"
    return "OtherAttack"


def load_csvs(
    csv_dir: str | Path,
    sample_per_file: int | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    csv_dir = Path(csv_dir)
    frames = []
    for path in sorted(csv_dir.glob("*.csv")):
        if sample_per_file:
            df = pd.read_csv(path)
            if len(df) > sample_per_file:
                df = df.sample(n=sample_per_file, random_state=random_state)
        else:
            df = pd.read_csv(path)
        df["source_file"] = path.name
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")
    df = pd.concat(frames, ignore_index=True)
    return prepare_dataframe(df)


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    if "label" not in df.columns:
        raise ValueError("Expected a 'label' column")
    df["label"] = df["label"].astype(str).str.strip()
    df["binary_label"] = (df["label"] != "Benign").astype(int)
    df["attack_family"] = df["label"].map(attack_family)
    if "timestamp" in df.columns:
        df["timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["day"] = df["timestamp_dt"].dt.date.astype(str)
        df["hour"] = df["timestamp_dt"].dt.hour.fillna(-1).astype(int)
    else:
        df["timestamp_dt"] = pd.NaT
        df["day"] = "unknown"
        df["hour"] = -1

    numeric_candidates = [
        c
        for c in df.columns
        if c
        not in {
            "flow_id",
            "timestamp",
            "src_ip",
            "dst_ip",
            "label",
            "source_file",
            "attack_family",
            "timestamp_dt",
            "day",
        }
    ]
    for col in numeric_candidates:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df


def save_prepared(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)


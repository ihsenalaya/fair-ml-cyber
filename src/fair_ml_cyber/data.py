"""Data loading and preprocessing."""

from __future__ import annotations

import re
from pathlib import Path
from zlib import adler32

import numpy as np
import pandas as pd


RARE_LABELS = {
    "Heartbleed",
    "Web_SQL_Injection",
    "Web_XSS",
    "Web_Brute_Force",
    "Brute Force -Web",
    "Brute Force -XSS",
    "SQL Injection",
}


def canonicalize_column_name(column: object) -> str:
    """Map CICFlowMeter-style headers to stable snake_case names."""
    name = str(column).strip().replace("\ufeff", "")
    name = name.replace("/", "_per_")
    name = re.sub(r"[^0-9A-Za-z]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_").lower()
    aliases = {
        "dst_port": "dst_port",
        "destination_port": "dst_port",
        "src_port": "src_port",
        "source_port": "src_port",
        "timestamp": "timestamp",
        "label": "label",
        "protocol": "protocol",
    }
    return aliases.get(name, name)


def attack_family(label: str) -> str:
    label = str(label).strip()
    lower = label.lower()
    compact = lower.replace("_", " ").replace("-", " ")

    if lower == "benign":
        return "Benign"
    if "ddos" in compact:
        return "DDoS"
    if "dos" in compact:
        return "DoS"
    if any(term in compact for term in ("web", "xss", "sql injection")):
        return "Web"
    if any(term in compact for term in ("patator", "bruteforce", "brute force", "ftp", "ssh")):
        return "BruteForce"
    if "portscan" in compact or "port scan" in compact:
        return "PortScan"
    if lower == "bot" or lower.startswith("botnet"):
        return "Botnet"
    if "heartbleed" in compact:
        return "Heartbleed"
    if "infilter" in compact or "infiltration" in compact:
        return "Infiltration"
    if "fuzzer" in compact:
        return "Fuzzers"
    if "analysis" in compact:
        return "Analysis"
    if "backdoor" in compact:
        return "Backdoor"
    if "exploit" in compact:
        return "Exploits"
    if "generic" in compact:
        return "Generic"
    if "reconnaissance" in compact:
        return "Reconnaissance"
    if "shellcode" in compact:
        return "Shellcode"
    if "worm" in compact:
        return "Worms"
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
            df = sample_csv(path, sample_per_file, random_state=random_state)
        else:
            df = pd.read_csv(path)
        df["source_file"] = path.name
        frames.append(df)
    if not frames:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")
    df = pd.concat(frames, ignore_index=True)
    return prepare_dataframe(df)


def sample_csv(
    path: str | Path,
    n: int,
    *,
    random_state: int = 42,
    chunksize: int = 100_000,
) -> pd.DataFrame:
    """Uniformly sample up to n rows from a CSV without loading the whole file."""
    path = Path(path)
    seed = random_state + adler32(path.name.encode("utf-8"))
    rng = np.random.default_rng(seed)
    reservoir: pd.DataFrame | None = None
    for chunk in pd.read_csv(path, chunksize=chunksize):
        chunk = chunk.copy()
        chunk["_sample_key"] = rng.random(len(chunk))
        if reservoir is None:
            reservoir = chunk
        else:
            reservoir = pd.concat([reservoir, chunk], ignore_index=True)
        if len(reservoir) > n:
            reservoir = reservoir.nsmallest(n, "_sample_key")
    if reservoir is None:
        return pd.DataFrame()
    return reservoir.drop(columns=["_sample_key"]).reset_index(drop=True)


def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [canonicalize_column_name(c) for c in df.columns]
    if "label" not in df.columns:
        raise ValueError("Expected a 'label' column")
    df["label"] = df["label"].astype(str).str.strip()
    df = df[df["label"].str.lower() != "label"].copy()
    df["binary_label"] = (df["label"] != "Benign").astype(int)
    df["attack_family"] = df["label"].map(attack_family)
    if "timestamp" in df.columns:
        df["timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)
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

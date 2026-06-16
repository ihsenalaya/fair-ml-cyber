"""Stable hashing utilities for reproducibility."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


def hash_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def hash_directory(directory: str | Path, pattern: str = "*.csv") -> str:
    directory = Path(directory)
    h = hashlib.sha256()
    for path in sorted(directory.glob(pattern)):
        h.update(path.name.encode("utf-8"))
        h.update(hash_file(path).encode("utf-8"))
    return h.hexdigest()[:16]


def hash_dataframe(df: pd.DataFrame) -> str:
    content = pd.util.hash_pandas_object(df, index=True).values.tobytes()
    return hashlib.sha256(content).hexdigest()[:16]


def hash_object(obj: object) -> str:
    data = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16]


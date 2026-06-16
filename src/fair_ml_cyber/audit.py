"""Dataset audit for CICIDS2017-like CSV files."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pandas as pd

from fair_ml_cyber.hashing import hash_directory


def audit_csv_dir(csv_dir: str | Path, output_dir: str | Path | None = None) -> dict:
    csv_dir = Path(csv_dir)
    files = sorted(csv_dir.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {csv_dir}")

    file_rows = []
    total_labels: Counter[str] = Counter()
    schema_hashes: Counter[tuple[str, ...]] = Counter()
    required = [
        "flow_id",
        "timestamp",
        "src_ip",
        "src_port",
        "dst_ip",
        "dst_port",
        "protocol",
        "label",
    ]

    for path in files:
        labels: Counter[str] = Counter()
        rows = 0
        ts_min = None
        ts_max = None
        with path.open("r", newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            header = next(reader)
            schema_hashes[tuple(header)] += 1
            label_idx = header.index("label")
            ts_idx = header.index("timestamp") if "timestamp" in header else None
            for row in reader:
                if not row:
                    continue
                rows += 1
                label = row[label_idx].strip()
                labels[label] += 1
                total_labels[label] += 1
                if ts_idx is not None and len(row) > ts_idx:
                    ts = row[ts_idx].strip()
                    if ts:
                        ts_min = ts if ts_min is None or ts < ts_min else ts_min
                        ts_max = ts if ts_max is None or ts > ts_max else ts_max
        file_rows.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "rows": rows,
                "columns": len(header),
                "labels": dict(labels),
                "timestamp_min": ts_min,
                "timestamp_max": ts_max,
            }
        )

    schema = list(schema_hashes.keys())[0]
    missing_required = [c for c in required if c not in schema]
    total_rows = sum(r["rows"] for r in file_rows)
    label_rows = [
        {"label": label, "rows": count, "pct": count / total_rows * 100.0}
        for label, count in total_labels.most_common()
    ]
    result = {
        "csv_dir": str(csv_dir),
        "data_hash": hash_directory(csv_dir),
        "num_files": len(files),
        "total_rows": total_rows,
        "unique_schemas": len(schema_hashes),
        "columns": list(schema),
        "missing_required_columns": missing_required,
        "files": file_rows,
        "labels": label_rows,
    }

    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(file_rows).to_csv(output_dir / "file_summary.csv", index=False)
        pd.DataFrame(label_rows).to_csv(output_dir / "label_distribution.csv", index=False)
        pd.DataFrame({"column": list(schema)}).to_csv(output_dir / "columns.csv", index=False)
        with open(output_dir / "audit_summary.json", "w", encoding="utf-8") as f:
            import json

            json.dump(result, f, indent=2, default=str)
    return result


"""Command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.experiment import run_smoke


def main() -> None:
    parser = argparse.ArgumentParser(prog="fair-ml-cyber")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Audit raw CSV files")
    audit.add_argument("--csv-dir", required=True, type=Path)
    audit.add_argument("--output-dir", required=True, type=Path)

    smoke = sub.add_parser("run-smoke", help="Run a sampled reproducibility smoke experiment")
    smoke.add_argument("--csv-dir", required=True, type=Path)
    smoke.add_argument("--work-dir", required=True, type=Path)
    smoke.add_argument("--sample-per-file", type=int, default=2000)
    smoke.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.command == "audit":
        result = audit_csv_dir(args.csv_dir, args.output_dir)
    elif args.command == "run-smoke":
        result = run_smoke(args.csv_dir, args.work_dir, args.sample_per_file, args.seed)
    else:
        raise ValueError(args.command)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()


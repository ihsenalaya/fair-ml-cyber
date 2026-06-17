"""Command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.advanced import run_advanced_analysis
from fair_ml_cyber.calibration import run_calibration_baselines
from fair_ml_cyber.experiment import run_experiment, run_smoke
from fair_ml_cyber.open_set import run_open_set_baselines


def _csv_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


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

    experiment = sub.add_parser("run-experiment", help="Run a configurable experiment")
    experiment.add_argument("--csv-dir", required=True, type=Path)
    experiment.add_argument("--work-dir", required=True, type=Path)
    experiment.add_argument("--sample-per-file", type=int, default=None)
    experiment.add_argument("--seed", type=int, default=42)
    experiment.add_argument(
        "--models",
        type=_csv_list,
        default=_csv_list("logistic_regression,random_forest,hist_gradient_boosting"),
    )
    experiment.add_argument(
        "--feature-tiers",
        type=_csv_list,
        default=_csv_list("no_identity,deployment_safe"),
    )
    experiment.add_argument(
        "--splits",
        type=_csv_list,
        default=_csv_list(
            "random_stratified,temporal,latest_day_holdout,"
            "scenario_holdout_Web,endpoint_pair_holdout"
        ),
    )
    experiment.add_argument("--result-prefix", default="experiment")
    experiment.add_argument("--no-save-models", action="store_true")
    experiment.add_argument("--no-save-prepared", action="store_true")

    advanced = sub.add_parser("run-advanced", help="Run article-level advanced analyses")
    advanced.add_argument("--csv-dir", required=True, type=Path)
    advanced.add_argument("--work-dir", required=True, type=Path)
    advanced.add_argument("--sample-per-file", type=int, default=None)
    advanced.add_argument("--seed", type=int, default=42)
    advanced.add_argument(
        "--models",
        type=_csv_list,
        default=_csv_list("logistic_regression,hist_gradient_boosting"),
    )
    advanced.add_argument(
        "--feature-tiers",
        type=_csv_list,
        default=_csv_list("no_identity,deployment_safe"),
    )
    advanced.add_argument(
        "--splits",
        type=_csv_list,
        default=_csv_list(
            "random_stratified,temporal,latest_day_holdout,"
            "scenario_holdout_Web,endpoint_pair_holdout"
        ),
    )
    advanced.add_argument(
        "--unknown-families",
        type=_csv_list,
        default=_csv_list("Web,Botnet,PortScan,DDoS"),
    )
    advanced.add_argument("--result-prefix", default="advanced")
    advanced.add_argument("--explain-sample-size", type=int, default=5000)
    advanced.add_argument("--permutation-repeats", type=int, default=2)

    open_set = sub.add_parser("run-open-set-baselines", help="Run open-set baseline analyses")
    open_set.add_argument("--csv-dir", required=True, type=Path)
    open_set.add_argument("--work-dir", required=True, type=Path)
    open_set.add_argument("--sample-per-file", type=int, default=None)
    open_set.add_argument("--seed", type=int, default=42)
    open_set.add_argument(
        "--models",
        type=_csv_list,
        default=_csv_list("isolation_forest"),
    )
    open_set.add_argument(
        "--feature-tiers",
        type=_csv_list,
        default=_csv_list("deployment_safe"),
    )
    open_set.add_argument(
        "--unknown-families",
        type=_csv_list,
        default=_csv_list("Web,Botnet,PortScan,DDoS"),
    )
    open_set.add_argument("--result-prefix", default="open_set_baselines")

    calibration = sub.add_parser(
        "run-calibration-baselines",
        help="Run post-hoc binary calibration baselines",
    )
    calibration.add_argument("--csv-dir", required=True, type=Path)
    calibration.add_argument("--work-dir", required=True, type=Path)
    calibration.add_argument("--sample-per-file", type=int, default=None)
    calibration.add_argument("--seed", type=int, default=42)
    calibration.add_argument(
        "--models",
        type=_csv_list,
        default=_csv_list("logistic_regression,hist_gradient_boosting"),
    )
    calibration.add_argument(
        "--feature-tiers",
        type=_csv_list,
        default=_csv_list("deployment_safe"),
    )
    calibration.add_argument(
        "--splits",
        type=_csv_list,
        default=_csv_list(
            "random_stratified,temporal,latest_day_holdout,"
            "scenario_holdout_Web,endpoint_pair_holdout"
        ),
    )
    calibration.add_argument("--result-prefix", default="calibration_baselines")

    args = parser.parse_args()

    if args.command == "audit":
        result = audit_csv_dir(args.csv_dir, args.output_dir)
    elif args.command == "run-smoke":
        result = run_smoke(args.csv_dir, args.work_dir, args.sample_per_file, args.seed)
    elif args.command == "run-experiment":
        result = run_experiment(
            args.csv_dir,
            args.work_dir,
            sample_per_file=args.sample_per_file,
            seed=args.seed,
            models=args.models,
            feature_tiers=args.feature_tiers,
            split_protocols=args.splits,
            result_prefix=args.result_prefix,
            save_models=not args.no_save_models,
            save_prepared_data=not args.no_save_prepared,
        )
    elif args.command == "run-advanced":
        result = run_advanced_analysis(
            args.csv_dir,
            args.work_dir,
            sample_per_file=args.sample_per_file,
            seed=args.seed,
            models=args.models,
            feature_tiers=args.feature_tiers,
            split_protocols=args.splits,
            unknown_families=args.unknown_families,
            result_prefix=args.result_prefix,
            explain_sample_size=args.explain_sample_size,
            permutation_repeats=args.permutation_repeats,
        )
    elif args.command == "run-open-set-baselines":
        result = run_open_set_baselines(
            args.csv_dir,
            args.work_dir,
            sample_per_file=args.sample_per_file,
            seed=args.seed,
            models=args.models,
            feature_tiers=args.feature_tiers,
            unknown_families=args.unknown_families,
            result_prefix=args.result_prefix,
        )
    elif args.command == "run-calibration-baselines":
        result = run_calibration_baselines(
            args.csv_dir,
            args.work_dir,
            sample_per_file=args.sample_per_file,
            seed=args.seed,
            models=args.models,
            feature_tiers=args.feature_tiers,
            split_protocols=args.splits,
            result_prefix=args.result_prefix,
        )
    else:
        raise ValueError(args.command)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

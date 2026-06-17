# Evidence Snapshot - `advanced-core-s7-001`

This directory contains the small text artifacts needed to verify the full-data advanced analyses for seed 7 without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/advanced-core-s7-001/named-outputs/work_dir/advanced_results/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `f37547920caba643536a5d92e7328621483d31007af442ed18ff85231277de55` |
| `advanced_core_s7_summary.json` | Advanced analysis summary JSON | 44 | `020bfa5cc2895236a1c302fa2ac2166e05632c1d73e85dd2b478bf8ad14a5622` |
| `advanced_core_s7_events.jsonl` | Advanced event log | 58 | `0a13fec15d7e29440abeea0ec917797ec6ebaa65c27ebc1d013c1c6bf4bf3af4` |
| `advanced_core_s7_binary_results.csv` | Binary transfer/calibration metrics | 11 | `01ee352ffd262ecb8eb49f311c8627f18e3442e200d9140501339faf029974b0` |
| `advanced_core_s7_multiclass_results.csv` | Multiclass label metrics | 11 | `bcff0821eeb7aeb19e9147fc7e0011984a114de94803b5f1fea1c9d4a6d3f3b9` |
| `advanced_core_s7_per_class_results.csv` | Per-class multiclass metrics | 133 | `d8abcb82a1fc999003f6c27377681a611147e468ad7e6f07d19233e87ece3a92` |
| `advanced_core_s7_rare_class_results.csv` | Rare-class subset | 35 | `8b169431385763b80a64c8466bb48f59cdc0a8e56bf336d7e7376256ff276fdc` |
| `advanced_core_s7_open_set_results.csv` | Unknown-family open-set metrics | 9 | `31da09e61c5a9b5d1a3294105c175ad7b2863e1e7fd44ed9566afe1bb1d62982` |
| `advanced_core_s7_calibration_bins.csv` | Reliability bins | 101 | `8af418d73534b17fbf30eaebbac54fc37fc3a923bf80d9f7e067649b49ab6396` |
| `advanced_core_s7_abstention_curves.csv` | Selective prediction curves | 61 | `46f48afd15816d1a3d7f5c457894b85499df161868d1ab7fa489f64685fe390f` |
| `advanced_core_s7_feature_importance.csv` | LR coefficients and HGB permutation importance | 1,151 | `516701c16f05bb4e0ab0234d6cf9dfb9c10ea50011c7dc942e81fec057859bfb` |
| `advanced_core_s7_explanation_stability.csv` | Top-15 explanation-overlap stability | 9 | `380652a800a8861bc442f4a26d707e42bd1988437f154824885f359a7a7d622d` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- seed 7;
- feature tier `deployment_safe`;
- 10 binary runs;
- 10 multiclass runs;
- 8 open-set runs;
- 0 skipped splits;
- binary `warning_count` sum 0 and `convergence_warning_count` sum 0;
- multiclass `warning_count` sum 0 and `convergence_warning_count` sum 0.

Key checks:

- HGB binary macro-F1 is 0.9960 on `random_stratified`, 0.2300 on `temporal`, 0.3676 on `day_holdout_2017-07-07`, 0.4969 on `scenario_holdout_Web`, and 0.9916 on `endpoint_pair_holdout`.
- LR binary macro-F1 is 0.9345 on `random_stratified`, 0.5395 on `temporal`, 0.6358 on `day_holdout_2017-07-07`, 0.4823 on `scenario_holdout_Web`, and 0.8654 on `endpoint_pair_holdout`.
- HGB multiclass macro-F1 is 0.7033 on `random_stratified`, but only 0.0496 on `temporal`.
- LR multiclass macro-F1 is 0.4489 on `random_stratified`, but only 0.0453 on `temporal`.

The Azure user log had 8 sklearn `UserWarning` messages related to shifted multiclass support, 0 `ConvergenceWarning` messages and 0 tracebacks.

The full operational logs remain under `data/azure_jobs/advanced-core-s7-001/` locally and are intentionally not tracked by Git.

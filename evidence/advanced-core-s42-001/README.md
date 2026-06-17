# Evidence Snapshot - `advanced-core-s42-001`

This directory contains the small text artifacts needed to verify the full-data advanced analyses without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/advanced-core-s42-001/named-outputs/work_dir/advanced_results/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `b6854df35d84db3aed2da9e77dee32a660ce375d1528d9d0f84c76c741ed179c` |
| `advanced_core_s42_summary.json` | Advanced analysis summary JSON | 44 | `4f3eb41640dd03127a1e4584ba389ec2c165aed4cbdee3ce46d8b117d2128b38` |
| `advanced_core_s42_events.jsonl` | Advanced event log | 58 | `d261b182b5dd87b6295f4ee513e1a56025d175a88a7bd7487e24a3bea8532219` |
| `advanced_core_s42_binary_results.csv` | Binary transfer/calibration metrics | 11 | `3c417ba5dd70579a9ac19db94995a9da00f1baaa2a72b47a7b873406680e3982` |
| `advanced_core_s42_multiclass_results.csv` | Multiclass label metrics | 11 | `6a3258bbead02506c997ae447363627d2c9b28338da4a5ee2c9dd86f9e819297` |
| `advanced_core_s42_per_class_results.csv` | Per-class multiclass metrics | 135 | `bee5783011ae32d99d2453bc4b50a291cd07c406015c1c5222e4f4eefec54331` |
| `advanced_core_s42_rare_class_results.csv` | Rare-class subset | 37 | `65242b717b5fbc8ed6bced72a7b33b50fa9c4d9188c2982da4c29e1baf25f922` |
| `advanced_core_s42_open_set_results.csv` | Unknown-family open-set metrics | 9 | `e98ec867bd9cbb5de625809f56e91fa3d0d4e71ac3659c204e42856cd4719658` |
| `advanced_core_s42_calibration_bins.csv` | Reliability bins | 101 | `f2836138870a8493b74d58f182172371bd9d6430106c223b3f57cd04355e2727` |
| `advanced_core_s42_abstention_curves.csv` | Selective prediction curves | 61 | `7ed4269cdc52b79b9ea0305e19a8fdf6b77eaa7eb43f5cbc42d7b0ff38e71495` |
| `advanced_core_s42_feature_importance.csv` | LR coefficients and HGB permutation importance | 1,151 | `63b3295bf023553740590c392ebc22075953d178bc5bd6e5bc49b70ae5eb3b17` |
| `advanced_core_s42_explanation_stability.csv` | Top-15 explanation-overlap stability | 9 | `210ece0ae0e70cf419ea904e95023470bc6097909ec293ee2f78d00f4c353e1b` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- run data hash `171746c8753403c4`;
- seed 42;
- feature tier `deployment_safe`;
- 10 binary runs;
- 10 multiclass runs;
- 8 open-set runs;
- 0 skipped splits;
- binary `warning_count` sum 0 and `convergence_warning_count` sum 0;
- multiclass `warning_count` sum 0 and `convergence_warning_count` sum 0.

Operational warnings observed in the Azure user log:

- 16 occurrences of sklearn `UserWarning: y_pred contains classes not in y_true` during multiclass/per-class evaluation under shifted splits;
- 1 pandas `FutureWarning` in feature-importance concatenation;
- 0 sklearn `ConvergenceWarning` occurrences.

The full operational logs remain under `data/azure_jobs/advanced-core-s42-001/` locally and are intentionally not tracked by Git.

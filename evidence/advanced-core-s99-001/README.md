# Evidence Snapshot - `advanced-core-s99-001`

This directory contains the small text artifacts needed to verify the full-data advanced analyses for seed 99 without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/advanced-core-s99-001/named-outputs/work_dir/advanced_results/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `e5e5177ae328e12d21747996e4e6c0c9fb07f15c5f1ff223559e27a00047915a` |
| `advanced_core_s99_summary.json` | Advanced analysis summary JSON | 44 | `5ff705c33926672a466cfed6e3c46d2ad585e85df80e0e72332e03f164351467` |
| `advanced_core_s99_events.jsonl` | Advanced event log | 58 | `72d7c2bedfa37f79c7c05a784b88ae45454198eabec7495abbdc4ec9c59aced5` |
| `advanced_core_s99_binary_results.csv` | Binary transfer/calibration metrics | 11 | `9c93efbf1d27a6ba452681c9f072b06b6014d08ecdc9d15f64613599106c7759` |
| `advanced_core_s99_multiclass_results.csv` | Multiclass label metrics | 11 | `60ddb1895a1ed3848eff0e6dc9b7f400e2927dc58c101d629e4fa1714526b919` |
| `advanced_core_s99_per_class_results.csv` | Per-class multiclass metrics | 134 | `4a0405f4a101828ce66b26cb44d909d9050449641f1f17f691b1330a831f7ef6` |
| `advanced_core_s99_rare_class_results.csv` | Rare-class subset | 35 | `3b829313329819382d07dabab32548f5dd53cb8a8ab3aba1ddf65f34578f71bb` |
| `advanced_core_s99_open_set_results.csv` | Unknown-family open-set metrics | 9 | `b8a54d3c24881bb7eaba4f4b2e64a3292be33a986c2a7d2eb03de32e86922cb5` |
| `advanced_core_s99_calibration_bins.csv` | Reliability bins | 101 | `2664e2d3bad3e56981c23d78ffc19127fa5785e860a7d23603b57a44983083dd` |
| `advanced_core_s99_abstention_curves.csv` | Selective prediction curves | 61 | `f0f38f2ec5fdc80bf9a4cdf8ccf2f8de776adfb51a869ed2a7956887eb48dea5` |
| `advanced_core_s99_feature_importance.csv` | LR coefficients and HGB permutation importance | 1,151 | `52cf7653b60976371eb7b4f2b132c8ebc82a21f3d300226abd5af2abd67101aa` |
| `advanced_core_s99_explanation_stability.csv` | Top-15 explanation-overlap stability | 9 | `fdd92e592d4c300121231348e88027e7bddc316a0239af1862af37c601b7a9a5` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- seed 99;
- feature tier `deployment_safe`;
- 10 binary runs;
- 10 multiclass runs;
- 8 open-set runs;
- 0 skipped splits;
- binary `warning_count` sum 0 and `convergence_warning_count` sum 0;
- multiclass `warning_count` sum 0 and `convergence_warning_count` sum 0.

Key checks:

- HGB binary macro-F1 is 0.9958 on `random_stratified`, 0.2297 on `temporal`, 0.3678 on `day_holdout_2017-07-07`, 0.4976 on `scenario_holdout_Web`, and 0.9828 on `endpoint_pair_holdout`.
- LR binary macro-F1 is 0.9339 on `random_stratified`, 0.5395 on `temporal`, 0.6405 on `day_holdout_2017-07-07`, 0.4834 on `scenario_holdout_Web`, and 0.8931 on `endpoint_pair_holdout`.
- HGB multiclass macro-F1 is 0.7196 on `random_stratified`, but only 0.0414 on `temporal`.
- LR multiclass macro-F1 is 0.4522 on `random_stratified`, but only 0.0453 on `temporal`.

The full operational logs remain under `data/azure_jobs/advanced-core-s99-001/` locally and are intentionally not tracked by Git.

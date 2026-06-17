# Full-Data Core Multi-Seed Results

This file compares the verified full-data memory runs currently available:

- `fullcore-mem-s42-001`
- `fullcore-mem-s7-001`
- `fullcore-mem-s99-001`

All three runs use the full dataset, the same binary task, the same two models, the same two feature tiers, and the same five split protocols. These results improve the empirical basis of the article, but they still do not replace the missing rare-class, multi-class, open-set, calibration/abstention and explanation-stability experiments.

## Run Scope

| Item | Seed 42 | Seed 7 | Seed 99 |
|---|---|---|---|
| Azure ML job | `fullcore-mem-s42-001` | `fullcore-mem-s7-001` | `fullcore-mem-s99-001` |
| Git commit | `0a4808be5f5f5edf487767eb2496b3591c5ab98b` | `aacac54b9c1668347141688eeb81e3f35737e444` | `b98e5ce81ddac90351801acc15641df0f16a3f6f` |
| Git dirty flag | `False` | `False` | `False` |
| Compute | `cpu-memory-cluster`, `Standard_E8ds_v5` | `cpu-memory-cluster`, `Standard_E8ds_v5` | `cpu-memory-cluster`, `Standard_E8ds_v5` |
| Rows | 2,438,052 | 2,438,052 | 2,438,052 |
| Runs | 20 | 20 | 20 |
| Completed / failed | 20 / 0 | 20 / 0 | 20 / 0 |
| Stream duration | 43:42.95 | 45:51.80 | 45:59.45 |
| Download duration | 3:04.15 | 3:06.89 | 3:01.85 |
| Local artifact size | 3.4 MB | 3.5 MB | 3.5 MB |
| Tracked evidence | `evidence/fullcore-mem-s42-001/` | `evidence/fullcore-mem-s7-001/` | `evidence/fullcore-mem-s99-001/` |

## Overall Metrics By Seed

| Seed | Runs | Macro-F1 mean | Macro-F1 std | AUROC mean | AUPRC mean | Train s mean |
|---|---:|---:|---:|---:|---:|---:|
| 7 | 20 | 0.661384 | 0.263053 | 0.922222 | 0.760538 | 109.846 |
| 42 | 20 | 0.664466 | 0.267484 | 0.929869 | 0.771429 | 108.649 |
| 99 | 20 | 0.663620 | 0.264525 | 0.932339 | 0.774164 | 113.373 |

## Mean Macro-F1 By Split Across Seeds

Values are averaged across both feature tiers and both seeds.

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9977 | 0.9357 |
| `endpoint_pair_holdout` | 0.9924 | 0.8820 |
| `temporal` | 0.2315 | 0.5401 |
| `day_holdout_2017-07-07` | 0.4090 | 0.6394 |
| `scenario_holdout_Web` | 0.5207 | 0.4831 |

## Inter-Seed Standard Deviation

Values are macro-F1 standard deviations across seeds, after averaging the two feature tiers inside each seed.

| Split | HistGradientBoosting std | LogisticRegression std |
|---|---:|---:|
| `random_stratified` | 0.0020 | 0.0011 |
| `endpoint_pair_holdout` | 0.0060 | 0.0130 |
| `temporal` | 0.0025 | 0.0001 |
| `day_holdout_2017-07-07` | 0.0624 | 0.0023 |
| `scenario_holdout_Web` | 0.0497 | 0.0006 |

## Seed-Specific Macro-F1

### Seed 42

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9978 | 0.9364 |
| `endpoint_pair_holdout` | 0.9955 | 0.8859 |
| `temporal` | 0.2316 | 0.5401 |
| `day_holdout_2017-07-07` | 0.3698 | 0.6388 |
| `scenario_holdout_Web` | 0.5653 | 0.4836 |

### Seed 7

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9978 | 0.9355 |
| `endpoint_pair_holdout` | 0.9950 | 0.8660 |
| `temporal` | 0.2328 | 0.5401 |
| `day_holdout_2017-07-07` | 0.4279 | 0.6385 |
| `scenario_holdout_Web` | 0.4977 | 0.4826 |

### Seed 99

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9976 | 0.9351 |
| `endpoint_pair_holdout` | 0.9867 | 0.8941 |
| `temporal` | 0.2302 | 0.5401 |
| `day_holdout_2017-07-07` | 0.4293 | 0.6410 |
| `scenario_holdout_Web` | 0.4990 | 0.4831 |

## CTS Macro-F1 Across Seeds

`CTS_macro_F1 = macro_F1_stress_split / macro_F1_random_stratified` for the same model and seed. The table reports mean and standard deviation across seeds.

| Target split | Model | CTS mean | CTS std |
|---|---|---:|---:|
| `endpoint_pair_holdout` | HistGradientBoosting | 0.9946 | 0.0048 |
| `temporal` | HistGradientBoosting | 0.2321 | 0.0013 |
| `day_holdout_2017-07-07` | HistGradientBoosting | 0.4099 | 0.0341 |
| `scenario_holdout_Web` | HistGradientBoosting | 0.5219 | 0.0387 |
| `endpoint_pair_holdout` | LogisticRegression | 0.9426 | 0.0155 |
| `temporal` | LogisticRegression | 0.5772 | 0.0004 |
| `day_holdout_2017-07-07` | LogisticRegression | 0.6834 | 0.0018 |
| `scenario_holdout_Web` | LogisticRegression | 0.5163 | 0.0004 |

## Robust Random-vs-Stress Statistics

The snapshot `evidence/q1-stats-fullcore-multiseed-001/` adds bootstrap 95% confidence intervals and exact paired sign-flip tests over the six paired experimental units available per model: 3 seeds x 2 feature tiers. These intervals are over experimental units, not over individual flows.

| Model | Stress split | Mean delta vs random | 95% CI delta | Mean ratio | 95% CI ratio | p-value |
|---|---|---:|---:|---:|---:|---:|
| HistGradientBoosting | `temporal` | -0.7662 | [-0.7674, -0.7650] | 0.2320 | [0.2307, 0.2337] | 0.03125 |
| HistGradientBoosting | `day_holdout_2017-07-07` | -0.5887 | [-0.6281, -0.5486] | 0.4099 | [0.3697, 0.4505] | 0.03125 |
| HistGradientBoosting | `scenario_holdout_Web` | -0.4770 | [-0.4996, -0.4353] | 0.5219 | [0.4993, 0.5634] | 0.03125 |
| HistGradientBoosting | `endpoint_pair_holdout` | -0.0054 | [-0.0089, -0.0020] | 0.9946 | [0.9906, 0.9980] | 0.03125 |
| LogisticRegression | `temporal` | -0.3956 | [-0.3964, -0.3947] | 0.5772 | [0.5767, 0.5777] | 0.03125 |
| LogisticRegression | `day_holdout_2017-07-07` | -0.2963 | [-0.2980, -0.2947] | 0.6834 | [0.6817, 0.6851] | 0.03125 |
| LogisticRegression | `scenario_holdout_Web` | -0.4526 | [-0.4534, -0.4516] | 0.5163 | [0.5157, 0.5170] | 0.03125 |
| LogisticRegression | `endpoint_pair_holdout` | -0.0537 | [-0.0632, -0.0443] | 0.9426 | [0.9325, 0.9527] | 0.03125 |

All stress splits are worse than the paired random baseline for both models. The exact p-value is 0.03125 in every row because all six paired differences have the same sign; with only six pairs this is the smallest possible two-sided sign-flip p-value. Standardized effect sizes are available in the CSV, but they should be interpreted carefully because several groups have very low inter-seed variance.

## Interpretation

The main conclusion is stable across three seeds: random stratified evaluation is much more optimistic than temporal and day/scenario stress tests. HistGradientBoosting remains nearly perfect in random and endpoint-pair holdout, but collapses in temporal and day-holdout settings. LogisticRegression is weaker in random split, but more stable under temporal and day-holdout shifts.

The second conclusion is that repeated seeds matter. HistGradientBoosting varies noticeably on `day_holdout_2017-07-07` and `scenario_holdout_Web`, while LogisticRegression is almost unchanged on those splits. Endpoint-pair holdout also changes its test-set size and score by seed because endpoint groups are randomized. This should be reported as part of the article's robustness analysis rather than averaged away without discussion.

## Operational Issues

| Issue | Seed 42 | Seed 7 | Seed 99 | Article impact |
|---|---:|---:|---:|---|
| Historical LogisticRegression `ConvergenceWarning` count in the original `max_iter=500` core runs | 2 | 3 | 2 | These rows are historical evidence only for LR convergence claims |
| Corrected LR2000/nohour convergence-clean rerun | `fullcore-lr2000-s42-001` | `fullcore-lr2000-nohour-s7-001` | `fullcore-lr2000-nohour-s99-001` | Reviewer-facing LR convergence risk is resolved by the reruns documented in `LR2000_CONVERGENCE_RESULTS.md` |
| `az ml job show` timeout after completion | Yes | Not rerun after completion | Not rerun after completion | Use stream + artifacts as evidence |
| Runtime pip root-user warnings | Yes | Yes | Yes | Operational warning from image-only runtime workaround |

## Remaining Work

For a stronger Q1-level evidence base, the next empirical steps are:

- use the LR2000/nohour rerun artifacts for any final convergence-clean LR tables;
- keep the original `max_iter=500` LR rows labelled as historical if they are retained for comparison;
- extend external validation beyond the current CSE-CIC-IDS2018 sample if an independent official dataset becomes accessible;
- increase explanation-stability repeats and add uncertainty estimates if scope permits.

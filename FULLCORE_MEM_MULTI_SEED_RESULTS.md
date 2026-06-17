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

## Interpretation

The main conclusion is stable across three seeds: random stratified evaluation is much more optimistic than temporal and day/scenario stress tests. HistGradientBoosting remains nearly perfect in random and endpoint-pair holdout, but collapses in temporal and day-holdout settings. LogisticRegression is weaker in random split, but more stable under temporal and day-holdout shifts.

The second conclusion is that repeated seeds matter. HistGradientBoosting varies noticeably on `day_holdout_2017-07-07` and `scenario_holdout_Web`, while LogisticRegression is almost unchanged on those splits. Endpoint-pair holdout also changes its test-set size and score by seed because endpoint groups are randomized. This should be reported as part of the article's robustness analysis rather than averaged away without discussion.

## Operational Issues

| Issue | Seed 42 | Seed 7 | Seed 99 | Article impact |
|---|---:|---:|---:|---|
| LogisticRegression `ConvergenceWarning` count | 2 | 3 | 2 | LR needs either a tuned convergence protocol or an explicit limitation statement |
| `az ml job show` timeout after completion | Yes | Not rerun after completion | Not rerun after completion | Use stream + artifacts as evidence |
| Runtime pip root-user warnings | Yes | Yes | Yes | Operational warning from image-only runtime workaround |

## Remaining Work

For a stronger Q1-level evidence base, the next empirical steps are:

- decide whether LogisticRegression should be rerun with higher `max_iter` or alternative solver settings;
- add rare-class and multi-class analyses;
- implement open-set family holdout;
- add calibration/abstention figures and explanation-stability metrics.

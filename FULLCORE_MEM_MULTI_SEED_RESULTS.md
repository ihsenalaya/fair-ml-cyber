# Full-Data Core Multi-Seed Results

This file compares the verified full-data memory runs currently available:

- `fullcore-mem-s42-001`
- `fullcore-mem-s7-001`

Both runs use the full dataset, the same binary task, the same two models, the same two feature tiers, and the same five split protocols. These results improve the empirical basis of the article, but they still do not replace the missing rare-class, multi-class, open-set, calibration/abstention and explanation-stability experiments.

## Run Scope

| Item | Seed 42 | Seed 7 |
|---|---|---|
| Azure ML job | `fullcore-mem-s42-001` | `fullcore-mem-s7-001` |
| Git commit | `0a4808be5f5f5edf487767eb2496b3591c5ab98b` | `aacac54b9c1668347141688eeb81e3f35737e444` |
| Git dirty flag | `False` | `False` |
| Compute | `cpu-memory-cluster`, `Standard_E8ds_v5` | `cpu-memory-cluster`, `Standard_E8ds_v5` |
| Rows | 2,438,052 | 2,438,052 |
| Runs | 20 | 20 |
| Completed / failed | 20 / 0 | 20 / 0 |
| Stream duration | 43:42.95 | 45:51.80 |
| Download duration | 3:04.15 | 3:06.89 |
| Local artifact size | 3.4 MB | 3.5 MB |
| Tracked evidence | `evidence/fullcore-mem-s42-001/` | `evidence/fullcore-mem-s7-001/` |

## Overall Metrics By Seed

| Seed | Runs | Macro-F1 mean | Macro-F1 std | AUROC mean | AUPRC mean | Train s mean |
|---|---:|---:|---:|---:|---:|---:|
| 7 | 20 | 0.661384 | 0.263053 | 0.922222 | 0.760538 | 109.846 |
| 42 | 20 | 0.664466 | 0.267484 | 0.929869 | 0.771429 | 108.649 |

## Mean Macro-F1 By Split Across Seeds

Values are averaged across both feature tiers and both seeds.

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9978 | 0.9360 |
| `endpoint_pair_holdout` | 0.9952 | 0.8759 |
| `temporal` | 0.2322 | 0.5401 |
| `day_holdout_2017-07-07` | 0.3988 | 0.6386 |
| `scenario_holdout_Web` | 0.5315 | 0.4831 |

## Inter-Seed Standard Deviation

Values are macro-F1 standard deviations across seeds, after averaging the two feature tiers inside each seed.

| Split | HistGradientBoosting std | LogisticRegression std |
|---|---:|---:|
| `random_stratified` | 0.0020 | 0.0011 |
| `endpoint_pair_holdout` | 0.0041 | 0.0116 |
| `temporal` | 0.0029 | 0.0002 |
| `day_holdout_2017-07-07` | 0.0596 | 0.0024 |
| `scenario_holdout_Web` | 0.0604 | 0.0007 |

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

## CTS Macro-F1 Across Seeds

`CTS_macro_F1 = macro_F1_stress_split / macro_F1_random_stratified` for the same model and seed. The table reports mean and standard deviation across seeds.

| Target split | Model | CTS mean | CTS std |
|---|---|---:|---:|
| `endpoint_pair_holdout` | HistGradientBoosting | 0.9974 | 0.0003 |
| `temporal` | HistGradientBoosting | 0.2327 | 0.0008 |
| `day_holdout_2017-07-07` | HistGradientBoosting | 0.3997 | 0.0412 |
| `scenario_holdout_Web` | HistGradientBoosting | 0.5327 | 0.0479 |
| `endpoint_pair_holdout` | LogisticRegression | 0.9359 | 0.0144 |
| `temporal` | LogisticRegression | 0.5770 | 0.0004 |
| `day_holdout_2017-07-07` | LogisticRegression | 0.6823 | 0.0002 |
| `scenario_holdout_Web` | LogisticRegression | 0.5162 | 0.0005 |

## Interpretation

The main conclusion is stable across seeds: random stratified evaluation is much more optimistic than temporal and day/scenario stress tests. HistGradientBoosting remains nearly perfect in random and endpoint-pair holdout, but collapses in temporal and day-holdout settings. LogisticRegression is weaker in random split, but more stable under temporal and day-holdout shifts.

The second conclusion is that repeated seeds matter. HistGradientBoosting varies noticeably on `day_holdout_2017-07-07` and `scenario_holdout_Web`, while LogisticRegression is almost unchanged on those splits. This should be reported as part of the article's robustness analysis rather than averaged away without discussion.

## Operational Issues

| Issue | Seed 42 | Seed 7 | Article impact |
|---|---:|---:|---|
| LogisticRegression `ConvergenceWarning` count | 2 | 3 | LR needs either a tuned convergence protocol or an explicit limitation statement |
| `az ml job show` timeout after completion | Yes | Not rerun after completion | Use stream + artifacts as evidence |
| Runtime pip root-user warnings | Yes | Yes | Operational warning from image-only runtime workaround |

## Remaining Work

For a stronger Q1-level evidence base, the next empirical steps are:

- add at least one more seed or justify stopping at two seeds;
- decide whether LogisticRegression should be rerun with higher `max_iter` or alternative solver settings;
- add rare-class and multi-class analyses;
- implement open-set family holdout;
- add calibration/abstention figures and explanation-stability metrics.

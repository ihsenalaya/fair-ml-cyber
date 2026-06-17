# Advanced Core Multi-Seed Status

Date: 2026-06-17

This file summarizes the advanced analyses repeated on seeds 42, 7 and 99.

## Current Status

| Seed | Azure job | Status | Tracked evidence |
|---|---|---|---|
| 42 | `advanced-core-s42-001` | Completed | `evidence/advanced-core-s42-001/` |
| 7 | `advanced-core-s7-001` | Completed and downloaded | `evidence/advanced-core-s7-001/` |
| 99 | `advanced-core-s99-001` | Completed and downloaded | `evidence/advanced-core-s99-001/` |

C2 is closed for the requested three-seed advanced evidence. Each seed has binary, multiclass, per-class, rare-class, open-set, calibration-bin, abstention-curve, feature-importance and explanation-stability artifacts.

## Binary Macro-F1

| Seed | Model | Random | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.9370 | 0.5395 | 0.6370 | 0.4833 | 0.8837 |
| 42 | HistGradientBoosting | 0.9960 | 0.2296 | 0.3678 | 0.6218 | 0.9917 |
| 7 | LogisticRegression | 0.9345 | 0.5395 | 0.6358 | 0.4823 | 0.8654 |
| 7 | HistGradientBoosting | 0.9960 | 0.2300 | 0.3676 | 0.4969 | 0.9916 |
| 99 | LogisticRegression | 0.9339 | 0.5395 | 0.6405 | 0.4834 | 0.8931 |
| 99 | HistGradientBoosting | 0.9958 | 0.2297 | 0.3678 | 0.4976 | 0.9828 |

Mean macro-F1 across seeds:

| Model | Split | Mean | Std | Min | Max |
|---|---|---:|---:|---:|---:|
| HistGradientBoosting | `random_stratified` | 0.9959 | 0.0002 | 0.9958 | 0.9960 |
| HistGradientBoosting | `temporal` | 0.2298 | 0.0002 | 0.2296 | 0.2300 |
| HistGradientBoosting | `day_holdout_2017-07-07` | 0.3677 | 0.0002 | 0.3676 | 0.3678 |
| HistGradientBoosting | `scenario_holdout_Web` | 0.5387 | 0.0719 | 0.4969 | 0.6218 |
| HistGradientBoosting | `endpoint_pair_holdout` | 0.9887 | 0.0051 | 0.9828 | 0.9917 |
| LogisticRegression | `random_stratified` | 0.9351 | 0.0017 | 0.9339 | 0.9370 |
| LogisticRegression | `temporal` | 0.5395 | 0.0000 | 0.5395 | 0.5395 |
| LogisticRegression | `day_holdout_2017-07-07` | 0.6378 | 0.0024 | 0.6358 | 0.6405 |
| LogisticRegression | `scenario_holdout_Web` | 0.4830 | 0.0006 | 0.4823 | 0.4834 |
| LogisticRegression | `endpoint_pair_holdout` | 0.8807 | 0.0141 | 0.8654 | 0.8931 |

## Multiclass Macro-F1

| Seed | Model | Random | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.4487 | 0.0453 | 0.0546 | 0.0667 | 0.3044 |
| 42 | HistGradientBoosting | 0.7479 | 0.0415 | 0.0523 | 0.0762 | 0.4447 |
| 7 | LogisticRegression | 0.4489 | 0.0453 | 0.0546 | 0.0668 | 0.3230 |
| 7 | HistGradientBoosting | 0.7033 | 0.0496 | 0.0524 | 0.0763 | 0.4052 |
| 99 | LogisticRegression | 0.4522 | 0.0453 | 0.0545 | 0.0667 | 0.3479 |
| 99 | HistGradientBoosting | 0.7196 | 0.0414 | 0.0516 | 0.0708 | 0.5233 |

Mean multiclass macro-F1 across seeds:

| Model | Split | Mean | Std | Min | Max |
|---|---|---:|---:|---:|---:|
| HistGradientBoosting | `random_stratified` | 0.7236 | 0.0226 | 0.7033 | 0.7479 |
| HistGradientBoosting | `temporal` | 0.0441 | 0.0047 | 0.0414 | 0.0496 |
| HistGradientBoosting | `day_holdout_2017-07-07` | 0.0521 | 0.0005 | 0.0516 | 0.0524 |
| HistGradientBoosting | `scenario_holdout_Web` | 0.0744 | 0.0032 | 0.0708 | 0.0763 |
| HistGradientBoosting | `endpoint_pair_holdout` | 0.4577 | 0.0601 | 0.4052 | 0.5233 |
| LogisticRegression | `random_stratified` | 0.4499 | 0.0019 | 0.4487 | 0.4522 |
| LogisticRegression | `temporal` | 0.0453 | 0.0000 | 0.0453 | 0.0453 |
| LogisticRegression | `day_holdout_2017-07-07` | 0.0545 | 0.0000 | 0.0545 | 0.0546 |
| LogisticRegression | `scenario_holdout_Web` | 0.0667 | 0.0001 | 0.0667 | 0.0668 |
| LogisticRegression | `endpoint_pair_holdout` | 0.3251 | 0.0218 | 0.3044 | 0.3479 |

## Explanation Stability

Top-15 Jaccard overlap versus `random_stratified`:

| Seed | Model | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.5789 | 0.6667 | 0.5789 | 0.7647 |
| 42 | HistGradientBoosting | 0.0714 | 0.1538 | 0.1538 | 0.5000 |
| 7 | LogisticRegression | 0.5789 | 0.5789 | 0.5789 | 0.4286 |
| 7 | HistGradientBoosting | 0.2000 | 0.1538 | 0.2000 | 0.4286 |
| 99 | LogisticRegression | 0.7647 | 0.8750 | 0.5789 | 0.7647 |
| 99 | HistGradientBoosting | 0.1111 | 0.1538 | 0.2000 | 0.3636 |

Mean Jaccard across seeds:

| Model | Split | Mean | Std | Min | Max |
|---|---|---:|---:|---:|---:|
| HistGradientBoosting | `temporal` | 0.1275 | 0.0658 | 0.0714 | 0.2000 |
| HistGradientBoosting | `day_holdout_2017-07-07` | 0.1538 | 0.0000 | 0.1538 | 0.1538 |
| HistGradientBoosting | `scenario_holdout_Web` | 0.1846 | 0.0266 | 0.1538 | 0.2000 |
| HistGradientBoosting | `endpoint_pair_holdout` | 0.4307 | 0.0682 | 0.3636 | 0.5000 |
| LogisticRegression | `temporal` | 0.6409 | 0.1072 | 0.5789 | 0.7647 |
| LogisticRegression | `day_holdout_2017-07-07` | 0.7069 | 0.1521 | 0.5789 | 0.8750 |
| LogisticRegression | `scenario_holdout_Web` | 0.5789 | 0.0000 | 0.5789 | 0.5789 |
| LogisticRegression | `endpoint_pair_holdout` | 0.6527 | 0.1941 | 0.4286 | 0.7647 |

## Interpretation

The advanced evidence now supports the same qualitative conclusions across seeds 42, 7 and 99:

- binary random performance remains high while temporal and scenario stress tests expose large drops;
- multiclass macro-F1 collapses under temporal, latest-day and Web holdout splits for both models;
- HGB explanation overlap is consistently much lower than LR overlap under the hardest stress splits;
- the XAI analysis is still lightweight because HGB permutation importance used a small sample and low repeat count, so uncertainty intervals remain a recommended strengthening step rather than a hidden claim.

## Remaining Azure Queue Status

Latest checked status on 2026-06-17:

- `open-set-if-s7-001`: `Queued`
- `calibration-s42-001`: `Queued`
- `calibration-s7-001`: `Queued`
- `calibration-s99-001`: `Queued`
- `fullcore-lr2000-nohour-s42-001`: `Queued`
- `fullcore-lr2000-nohour-s7-001`: `Queued`
- `fullcore-lr2000-nohour-s99-001`: `Queued`

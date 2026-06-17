# Advanced Core Multi-Seed Status

Date: 2026-06-17

This file tracks progress toward repeating the advanced analyses on seeds 42, 7 and 99.

## Current Status

| Seed | Azure job | Status | Tracked evidence |
|---|---|---|---|
| 42 | `advanced-core-s42-001` | Completed | `evidence/advanced-core-s42-001/` |
| 99 | `advanced-core-s99-001` | Completed and downloaded | `evidence/advanced-core-s99-001/` |
| 7 | `advanced-core-s7-001` | Running on Azure ML | Not yet available |

C2 is therefore partially improved but not closed. The reviewer-facing claim still needs seed 7 before it can be described as 3-seed advanced evidence.

## Binary Macro-F1

| Seed | Model | Random | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.9370 | 0.5395 | 0.6370 | 0.4833 | 0.8837 |
| 42 | HistGradientBoosting | 0.9960 | 0.2296 | 0.3678 | 0.6218 | 0.9917 |
| 99 | LogisticRegression | 0.9339 | 0.5395 | 0.6405 | 0.4834 | 0.8931 |
| 99 | HistGradientBoosting | 0.9958 | 0.2297 | 0.3678 | 0.4976 | 0.9828 |

## Multiclass Macro-F1

| Seed | Model | Random | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.4487 | 0.0453 | 0.0546 | 0.0667 | 0.3044 |
| 42 | HistGradientBoosting | 0.7479 | 0.0415 | 0.0523 | 0.0762 | 0.4447 |
| 99 | LogisticRegression | 0.4522 | 0.0453 | 0.0545 | 0.0667 | 0.3479 |
| 99 | HistGradientBoosting | 0.7196 | 0.0414 | 0.0516 | 0.0708 | 0.5233 |

## Explanation Stability

Top-15 Jaccard overlap versus `random_stratified` remains model-dependent:

| Seed | Model | Temporal | Latest-day | Web holdout | Endpoint-pair |
|---:|---|---:|---:|---:|---:|
| 42 | LogisticRegression | 0.5789 | 0.6667 | 0.5789 | 0.7647 |
| 42 | HistGradientBoosting | 0.0714 | 0.1538 | 0.1538 | 0.5000 |
| 99 | LogisticRegression | 0.7647 | 0.8750 | 0.5789 | 0.7647 |
| 99 | HistGradientBoosting | 0.1111 | 0.1538 | 0.2000 | 0.3636 |

Interpretation: seed 99 supports the seed 42 observation that HGB feature-importance overlap is much less stable under stress splits than LR. This is still not enough for a final bootstrap/CI XAI claim because seed 7 and higher permutation repeats are missing.

## Azure Queue Status

Latest checked status on 2026-06-17:

- `advanced-core-s7-001`: `Running`
- `open-set-if-s7-001`: `Queued`
- `calibration-s42-001`: `Queued`
- `calibration-s7-001`: `Queued`
- `calibration-s99-001`: `Queued`
- `fullcore-lr2000-nohour-s42-001`: `Queued`
- `fullcore-lr2000-nohour-s7-001`: `Queued`
- `fullcore-lr2000-nohour-s99-001`: `Queued`

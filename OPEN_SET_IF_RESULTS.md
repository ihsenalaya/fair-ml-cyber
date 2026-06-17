# Full-Data Isolation Forest Open-Set Results

Date: 2026-06-17

This file summarizes the completed full-data Isolation Forest open-set baseline runs. These are separate from the uncertainty-based open-set analysis inside `advanced-core`.

Tracked evidence:

- `evidence/open-set-if-s42-001/`
- `evidence/open-set-if-s99-001/`

## Run Scope

| Item | Value |
|---|---|
| Dataset | 18 local CICIDS2017-like CSVs |
| Rows | 2,438,052 |
| Feature tier | `deployment_safe` |
| Model | `isolation_forest` |
| Unknown families | `Web`, `Botnet`, `PortScan`, `DDoS` |
| Completed seeds | 42, 99 |
| Pending seed | 7 |

## Metrics

| Seed | Unknown family | AUROC | AUPRC | Unknown recall at p90 review |
|---:|---|---:|---:|---:|
| 42 | Web | 0.6925 | 0.0188 | 0.0241 |
| 42 | Botnet | 0.7647 | 0.0437 | 0.1605 |
| 42 | PortScan | 0.9233 | 0.7074 | 0.2708 |
| 42 | DDoS | 0.9633 | 0.7155 | 0.3402 |
| 99 | Web | 0.5866 | 0.0142 | 0.0238 |
| 99 | Botnet | 0.7894 | 0.0568 | 0.7171 |
| 99 | PortScan | 0.9301 | 0.7295 | 0.3055 |
| 99 | DDoS | 0.9582 | 0.6930 | 0.3291 |

## Mean Across Completed Seeds

| Unknown family | Mean AUROC | AUROC std | Mean AUPRC | AUPRC std |
|---|---:|---:|---:|---:|
| Web | 0.6395 | 0.0749 | 0.0165 | 0.0033 |
| Botnet | 0.7771 | 0.0174 | 0.0503 | 0.0093 |
| PortScan | 0.9267 | 0.0048 | 0.7184 | 0.0156 |
| DDoS | 0.9607 | 0.0036 | 0.7042 | 0.0159 |

## Interpretation

Isolation Forest is a stronger open-set baseline than reporting only softmax/uncertainty behavior, but the completed results are mixed:

- strong AUROC for PortScan and DDoS;
- weak Web unknown detection, especially in AUPRC due to low support and class imbalance;
- unstable Botnet recall at the fixed p90 review rule across seeds 42 and 99.

The `open-set-if-s7-001` job is still queued, so this should be described as 2-seed evidence until seed 7 is downloaded.

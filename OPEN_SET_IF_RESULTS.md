# Full-Data Isolation Forest Open-Set Results

Date: 2026-06-17

This file summarizes the completed full-data Isolation Forest open-set baseline runs. These are separate from the uncertainty-based open-set analysis inside `advanced-core`.

Tracked evidence:

- `evidence/open-set-if-s42-001/`
- `evidence/open-set-if-s7-001/`
- `evidence/open-set-if-s99-001/`

## Run Scope

| Item | Value |
|---|---|
| Dataset | 18 local CICIDS2017-like CSVs |
| Rows | 2,438,052 |
| Feature tier | `deployment_safe` |
| Model | `isolation_forest` |
| Unknown families | `Web`, `Botnet`, `PortScan`, `DDoS` |
| Completed seeds | 42, 7, 99 |
| Pending seed | None |

## Metrics

| Seed | Unknown family | AUROC | AUPRC | Unknown recall at p90 review |
|---:|---|---:|---:|---:|
| 7 | Web | 0.7143 | 0.0204 | 0.0243 |
| 7 | Botnet | 0.7635 | 0.0421 | 0.0080 |
| 7 | PortScan | 0.8917 | 0.6438 | 0.1252 |
| 7 | DDoS | 0.9663 | 0.7319 | 0.3575 |
| 42 | Web | 0.6925 | 0.0188 | 0.0241 |
| 42 | Botnet | 0.7647 | 0.0437 | 0.1605 |
| 42 | PortScan | 0.9233 | 0.7074 | 0.2708 |
| 42 | DDoS | 0.9633 | 0.7155 | 0.3402 |
| 99 | Web | 0.5866 | 0.0142 | 0.0238 |
| 99 | Botnet | 0.7894 | 0.0568 | 0.7171 |
| 99 | PortScan | 0.9301 | 0.7295 | 0.3055 |
| 99 | DDoS | 0.9582 | 0.6930 | 0.3291 |

## Mean Across Completed Seeds

| Unknown family | Mean AUROC | AUROC std | Mean AUPRC | AUPRC std | Mean p90 recall | p90 recall std |
|---|---:|---:|---:|---:|---:|---:|
| Web | 0.6644 | 0.0683 | 0.0178 | 0.0032 | 0.0241 | 0.0002 |
| Botnet | 0.7725 | 0.0146 | 0.0475 | 0.0081 | 0.2952 | 0.3733 |
| PortScan | 0.9150 | 0.0205 | 0.6936 | 0.0445 | 0.2338 | 0.0957 |
| DDoS | 0.9626 | 0.0041 | 0.7134 | 0.0195 | 0.3423 | 0.0143 |

## Interpretation

Isolation Forest is a stronger open-set baseline than reporting only softmax/uncertainty behavior, but the completed results are mixed:

- strong AUROC for PortScan and DDoS;
- weak Web unknown detection, especially in AUPRC due to low support and class imbalance;
- unstable Botnet recall at the fixed p90 review rule across seeds.

The `open-set-if-s7-001` job is downloaded and tracked, so the Isolation Forest open-set baseline is now available for seeds 42, 7 and 99.

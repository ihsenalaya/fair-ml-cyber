# Evidence Snapshot - `open-set-if-s42-001`

This directory contains the text artifacts for the full-data Isolation Forest open-set baseline on seed 42.

Source artifact root:

`data/azure_jobs/open-set-if-s42-001/named-outputs/work_dir/open_set_results/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `642e2b6c0001e140dc92ba70ee53796be617d77d67246503bcf4d02909638d38` |
| `open_set_if_s42_summary.json` | Open-set summary JSON | 26 | `357309e1a9f5b9529645e07bd41501a603d54db88795414341806b29e54f37d3` |
| `open_set_if_s42_events.jsonl` | Open-set event log | 10 | `e73bf6d596e089ff336da88ee868a2f53c9983420f8f6412ec497d6f2fdc65a5` |
| `open_set_if_s42_results.csv` | Isolation Forest unknown-family metrics | 5 | `2399f2f9312b46864f5612c6b296c4a1316c383623ebd4c0bb2f5d8c5adbe7ed` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- model `isolation_forest`;
- feature tier `deployment_safe`;
- unknown families `Web`, `Botnet`, `PortScan`, `DDoS`;
- 4 completed rows and 0 failed rows.

| Unknown family | AUROC | AUPRC | Recall at p90 review |
|---|---:|---:|---:|
| `Web` | 0.6925 | 0.0188 | 0.0241 |
| `Botnet` | 0.7647 | 0.0437 | 0.1605 |
| `PortScan` | 0.9233 | 0.7074 | 0.2708 |
| `DDoS` | 0.9633 | 0.7155 | 0.3402 |

The full operational logs remain under `data/azure_jobs/open-set-if-s42-001/` locally and are intentionally not tracked by Git.

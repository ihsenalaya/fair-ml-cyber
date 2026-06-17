# Evidence Snapshot - `open-set-if-s99-001`

This directory contains the text artifacts for the full-data Isolation Forest open-set baseline on seed 99.

Source artifact root:

`data/azure_jobs/open-set-if-s99-001/named-outputs/work_dir/open_set_results/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `92b8b989c74f70675b6c20133bf2e524dd9ba046a28791fa1a1f6b2051368f6f` |
| `open_set_if_s99_summary.json` | Open-set summary JSON | 26 | `4fa37d20e704806cf5d165f7070ea83910016d8ca1dc2d5f4c27401aa8a5212b` |
| `open_set_if_s99_events.jsonl` | Open-set event log | 10 | `16bdb87d8249728587d2ebcb4484e77bcc0e4a767087fa5b9f1f36f6ff04cf9a` |
| `open_set_if_s99_results.csv` | Isolation Forest unknown-family metrics | 5 | `39565a562170dbea631819d218a60410ee69c1bae9d5a2e0e8846d5ed23b607c` |

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
| `Web` | 0.5866 | 0.0142 | 0.0238 |
| `Botnet` | 0.7894 | 0.0568 | 0.7171 |
| `PortScan` | 0.9301 | 0.7295 | 0.3055 |
| `DDoS` | 0.9582 | 0.6930 | 0.3291 |

The full operational logs remain under `data/azure_jobs/open-set-if-s99-001/` locally and are intentionally not tracked by Git.

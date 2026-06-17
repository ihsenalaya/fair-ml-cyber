# Evidence Snapshot - `fullcore-lr2000-s42-001`

This directory contains the small text artifacts needed to verify the LogisticRegression convergence rerun without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/fullcore-lr2000-s42-001/named-outputs/work_dir/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `c936c6f1eb2b556d639851698402ba03726dceebea083b0e29084ac3cc679efd` |
| `fullcore_lr2000_s42_results.csv` | Main result table, 10 completed LR/tier/split runs | 11 | `8b79102ad7645c8b18427ff32bd7481c21f4e5db08caa099578700d26ce39b5e` |
| `fullcore_lr2000_s42_summary.json` | Experiment summary JSON | 14 | `2ffaaa859692051b4eb1c87a35f3099e7c63ae1e81e65371787503a591725523` |
| `fullcore_lr2000_s42_events.jsonl` | Experiment event log, including warning counts | 22 | `2004c2ef376f2c78903346bb0f50ff8be0e19214e37e232188676cd6b3fddb95` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- run data hash `171746c8753403c4`;
- 10 planned LogisticRegression runs;
- 10 completed runs;
- 0 failed runs;
- 0 skipped splits;
- `warning_count` sum 0;
- `convergence_warning_count` sum 0.

This verifies that increasing LogisticRegression `max_iter` to 2000 removed the convergence warnings observed in the earlier seed 42 full-data LR fits, without inventing or retroactively changing the earlier results.

The full operational logs remain under `data/azure_jobs/fullcore-lr2000-s42-001/` locally and are intentionally not tracked by Git.

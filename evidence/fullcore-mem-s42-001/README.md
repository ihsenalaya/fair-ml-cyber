# Evidence Snapshot - `fullcore-mem-s42-001`

This directory contains the small text artifacts needed to verify the documented full-data core results without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/fullcore-mem-s42-001/named-outputs/work_dir/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `6bebacea86344449e8edaac1bafdb53c8d6ec2cfbb075b9077b8843bf8a80de0` |
| `fullcore_mem_s42_results.csv` | Main result table, 20 completed model/tier/split runs | 21 | `f4c1d81e1b17981aec955384ae8adcba19b4fe471b255b5c2ef4bfbe6f71041a` |
| `fullcore_mem_s42_summary.json` | Experiment summary JSON | 14 | `baaebaccc549c8d2a2114951ca922233927795a729485bd0fe08b94af75ccf3a` |
| `fullcore_mem_s42_events.jsonl` | Experiment event log, including run starts/completions | 42 | `8ef3f0562be064023fd21502924900fa632c4cf663a6d44b92a3edd2467a6fed` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- run data hash `171746c8753403c4`;
- 20 planned runs;
- 20 completed runs;
- 0 failed runs;
- 0 skipped splits.

The full operational logs remain under `data/azure_jobs/fullcore-mem-s42-001/` locally and are intentionally not tracked by Git.

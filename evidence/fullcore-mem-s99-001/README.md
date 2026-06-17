# Evidence Snapshot - `fullcore-mem-s99-001`

This directory contains the small text artifacts needed to verify the documented full-data core seed 99 results without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/fullcore-mem-s99-001/named-outputs/work_dir/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `b9d3af3defc54874d50bed37e61bddda9bceaf48863457816a290a677ca00bc8` |
| `fullcore_mem_s99_results.csv` | Main result table, 20 completed model/tier/split runs | 21 | `969ad923f85ceca0b5daa5d047d6027b724cdf9d901085ac988dd5caef9a835c` |
| `fullcore_mem_s99_summary.json` | Experiment summary JSON | 14 | `697624cead0bbd1c882a7fa4b1a6591ccdece9217b50320e45fd39bf49379272` |
| `fullcore_mem_s99_events.jsonl` | Experiment event log, including run starts/completions | 42 | `ec21a05ddd9ffb11eb656f5c6e4537bb0e0649c4e58152e58521809d96d0f412` |

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

The full operational logs remain under `data/azure_jobs/fullcore-mem-s99-001/` locally and are intentionally not tracked by Git.

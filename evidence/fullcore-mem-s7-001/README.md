# Evidence Snapshot - `fullcore-mem-s7-001`

This directory contains the small text artifacts needed to verify the documented full-data core seed 7 results without committing the full Azure ML artifact tree under `data/`.

Source artifact root:

`data/azure_jobs/fullcore-mem-s7-001/named-outputs/work_dir/`

## Files

| File | Purpose | Lines | SHA-256 |
|---|---|---:|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | 403 | `5d3c8d4768c727b649e3849416b9d525e77c8417c8c3f04619b3cc3822427d29` |
| `fullcore_mem_s7_results.csv` | Main result table, 20 completed model/tier/split runs | 21 | `76f8ce2ad2acb081edab78ebdd9cd6924ae89e241746d2548f1efe5f85609b53` |
| `fullcore_mem_s7_summary.json` | Experiment summary JSON | 14 | `ddd3fefe315d86a02aba8f0d76dda3e2349d0724058edefa0a53989cbb15b78d` |
| `fullcore_mem_s7_events.jsonl` | Experiment event log, including run starts/completions | 42 | `ab87e6f9898a4f4c66593b5ab2b862a353000a931fcabf9e4d89efde48ec614b` |

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

The full operational logs remain under `data/azure_jobs/fullcore-mem-s7-001/` locally and are intentionally not tracked by Git.

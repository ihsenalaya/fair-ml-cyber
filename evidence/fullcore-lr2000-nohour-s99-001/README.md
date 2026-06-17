# Evidence Snapshot - `fullcore-lr2000-nohour-s99-001`

This directory contains the small text artifacts needed to verify the corrected
LogisticRegression convergence rerun for seed 99, using `max_iter=2000` after
excluding the timestamp-derived `hour` feature from identity-safe tiers.

Source artifact root:

`data/azure_jobs/fullcore-lr2000-nohour-s99-001/named-outputs/work_dir/`

## Files

| File | Purpose | SHA-256 |
|---|---|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | `3ec7cc195705bfd4c4f28cf2f0ffb0838c18536600c1f6814b2c392fba89c60d` |
| `fullcore_lr2000_nohour_s99_results.csv` | Main result table, 10 completed LR/tier/split runs | `c7b463f9df5404efe8601ae0987ad8def6327cec7ff6e806a862e5ecf946bf89` |
| `fullcore_lr2000_nohour_s99_summary.json` | Experiment summary JSON | `3b4c824b9a6d1d4f81bd48a8aa55f89e2f35fc826af3e90cf2971522e6442b8b` |
| `fullcore_lr2000_nohour_s99_events.jsonl` | Experiment event log, including warning counts | `1ca209fe10888180adfc7abbc299b8c177ebd3ad9aa2ec517ce43c4abccb5f1b` |

## Verification

The copied artifacts show:

- 18 CSV files audited;
- 2,438,052 rows;
- full dataset hash `f51899df9bd60758`;
- 10 planned LogisticRegression runs;
- 10 completed runs;
- 0 failed runs;
- 0 skipped splits;
- `warning_count` sum 0;
- `convergence_warning_count` sum 0.

Together with `evidence/fullcore-lr2000-nohour-s7-001/`, this closes the
seed 7/99 LR2000/nohour convergence rerun requested for C3.

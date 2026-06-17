# Evidence Snapshot - `fullcore-lr2000-nohour-s7-001`

This directory contains the small text artifacts needed to verify the corrected
LogisticRegression convergence rerun for seed 7, using `max_iter=2000` after
excluding the timestamp-derived `hour` feature from identity-safe tiers.

Source artifact root:

`data/azure_jobs/fullcore-lr2000-nohour-s7-001/named-outputs/work_dir/`

## Files

| File | Purpose | SHA-256 |
|---|---|---|
| `audit_summary.json` | Dataset audit emitted by the Azure run | `55d8fb92a9601cae9d33de9445c3e6af60bcd734c842285ca4c39aa5fff4369b` |
| `fullcore_lr2000_nohour_s7_results.csv` | Main result table, 10 completed LR/tier/split runs | `6f23f4f80288cc6fe785967e2ea015d68c1d9a267138a841e952ce15f5e8ac8a` |
| `fullcore_lr2000_nohour_s7_summary.json` | Experiment summary JSON | `21d0e40d2b5e3939a8924c0bb8542c972b6d5737311c1624c16bc2657b2c8184` |
| `fullcore_lr2000_nohour_s7_events.jsonl` | Experiment event log, including warning counts | `6f153791be4c9f8da6f60240c4ff96190a553e1daefb2d97a3ec22ba24b48f5b` |

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

This closes the seed 7 side of the LR2000/nohour convergence rerun. Seed 99
must still be downloaded and verified before C3 is fully closed.

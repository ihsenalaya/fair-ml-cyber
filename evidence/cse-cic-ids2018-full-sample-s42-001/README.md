# CSE-CIC-IDS2018 Full-Sample External Validation Evidence

This directory tracks text artifacts for the larger external validation run on real CSE-CIC-IDS2018 CSV data.

Source:

- UNB CSE-CIC-IDS2018 official page: https://www.unb.ca/cic/datasets/ids-2018.html
- Public AWS prefix: `s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/`

Scope:

- 10 downloaded CICFlowMeter CSV files
- raw audited rows after repeated-header removal: 16,232,943
- raw data hash: `96cd4ce8a085248a`
- stratified validation sample rows: 363,648
- sample hash: `d3092e8e71a9680c`
- seed: 42

Artifacts:

- `raw_audit_summary.json`: audit of all downloaded raw CSV files.
- `raw_file_summary.csv`: raw file-level counts.
- `raw_label_distribution.csv`: raw label counts.
- `sample_summary.json`: stratified-sampling summary.
- `sample_audit_summary.json`: audit of the validation sample.
- `sample_file_summary.csv`: validation sample file-level counts.
- `sample_label_distribution.csv`: sampled label counts.
- `cse_cic2018_fullsample_s42_results.csv`: binary baseline results.
- `cse_cic2018_fullsample_s42_events.jsonl`: binary baseline event log.

## File Hashes

| File | Lines | SHA-256 |
|---|---:|---|
| `cse_cic2018_fullsample_s42_events.jsonl` | 26 | `7e5a98ed0425418b61219be3fa0fcf2d0e46f6086281838bf2c6c521de277459` |
| `cse_cic2018_fullsample_s42_results.csv` | 13 | `e5317429db7dcba712745922b8017fb418e2d5799e44e4139be5c9618fa41934` |
| `raw_audit_summary.json` | 301 | `330514a19c54054b0b5010942a3850b693948200037ccec20a273aef6eb77279` |
| `raw_file_summary.csv` | 11 | `1b155101ca34602942e23cb85aa173e40f627d2ac535925b471f90082b95544b` |
| `raw_label_distribution.csv` | 16 | `1dc25f3f2ae649c8f2d66cdcde03f0da2dfa33f4f33b3d8fb81a769d416fad97` |
| `sample_audit_summary.json` | 198 | `62b3da8cec758397b20a3661d714e4525afcd667dbcaad437876bef2308eecb6` |
| `sample_file_summary.csv` | 2 | `d5345f8203210c57a987138d12990ad9b06e2501982c51da68207cb108394244` |
| `sample_label_distribution.csv` | 16 | `c23ad96bd83b4984623451962fe5d82d0e86e96d46818bc4499a8655a6c01906` |
| `sample_summary.json` | 41 | `ac1827f3460c118f4dc5c6481594fdc7c778c07f23545650057d29bb66296bcc` |

## Binary Validation Results

The experiment used `deployment_safe` features, seed 42, and four valid split protocols: `random_stratified`, `temporal`, `latest_day_holdout`, and `scenario_holdout_Web`. `endpoint_pair_holdout` was deliberately excluded because endpoint identity columns are absent or incomplete in the public processed CSE-CIC-IDS2018 CSVs.

| Model | Random | Temporal | Latest-day 2018-03-02 | Web holdout |
|---|---:|---:|---:|---:|
| LogisticRegression | 0.8425 | 0.3913 | 0.4787 | 0.5522 |
| HistGradientBoosting | 0.9362 | 0.1037 | 0.8070 | 0.7161 |
| RandomForest | 0.9195 | 0.1050 | 0.8739 | 0.5779 |

All 12 runs completed with `warning_count=0` and `convergence_warning_count=0`.

This is a real-data external validation on the full downloaded CSE-CIC-IDS2018 processed CSV set, but it remains a capped stratified sample for tractable local execution. It should not be described as a full-prior benchmark over all 16.2M rows.

# CSE-CIC-IDS2018 Partial External Validation Evidence

This directory tracks text artifacts for the partial external validation run on real CSE-CIC-IDS2018 CSV data.

Source:

- UNB CSE-CIC-IDS2018 official page: https://www.unb.ca/cic/datasets/ids-2018.html
- Public AWS prefix: `s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/`

Scope:

- 5 downloaded CICFlowMeter CSV files
- raw audited rows after repeated-header removal: 4,525,400
- raw data hash: `414f7195ee1e137a`
- stratified validation sample rows: 200,928
- sample hash: `d90aca82728746b3`
- seed: 42

Artifacts:

- `raw_audit_summary.json`: audit of downloaded raw CSV files.
- `raw_label_distribution.csv`: raw label counts.
- `sample_summary.json`: stratified-sampling summary.
- `sample_audit_summary.json`: audit of the validation sample.
- `sample_label_distribution.csv`: sampled label counts.
- `cse_cic2018_partial_s42_results.csv`: binary baseline results.
- `cse_cic2018_partial_s42_summary.json`: binary baseline summary.
- `cse_cic2018_partial_s42_events.jsonl`: binary baseline event log.
- `cse_cic2018_calibration_partial_s42_results.csv`: raw/Platt/isotonic calibration results.
- `cse_cic2018_calibration_partial_s42_summary.json`: calibration summary.
- `cse_cic2018_calibration_partial_s42_events.jsonl`: calibration event log.
- `cse_cic2018_open_set_partial_s42_results.csv`: IsolationForest/LOF open-set results.
- `cse_cic2018_open_set_partial_s42_summary.json`: open-set summary.
- `cse_cic2018_open_set_partial_s42_events.jsonl`: open-set event log.

This is a real-data partial external validation. It is not synthetic and not a full CSE-CIC-IDS2018 benchmark.

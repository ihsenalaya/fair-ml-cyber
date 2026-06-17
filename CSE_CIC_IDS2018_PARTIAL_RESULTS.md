# CSE-CIC-IDS2018 Partial External Validation Results

Date: 2026-06-17

## Status Update

This was the first CSE-CIC-IDS2018 external validation pass. A larger follow-up using all 10 public processed CSV files and a 363,648-row real stratified sample is now documented in `CSE_CIC_IDS2018_FULL_SAMPLE_RESULTS.md` and `evidence/cse-cic-ids2018-full-sample-s42-001/`.

The calibration and open-set results below remain useful auxiliary evidence because those tasks have not yet been rerun on the larger 363,648-row sample.

## Source and Scope

External dataset source:

- CSE-CIC-IDS2018 official UNB page: https://www.unb.ca/cic/datasets/ids-2018.html
- Public AWS bucket prefix: `s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/`

This is a **partial external validation**, not a full CSE-CIC-IDS2018 benchmark. The purpose is to reduce the single-dataset risk of the paper by testing whether the random-vs-stress-split gap also appears on a real public external dataset.

Downloaded CSV files:

- `Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv`
- `Thursday-22-02-2018_TrafficForML_CICFlowMeter.csv`
- `Friday-23-02-2018_TrafficForML_CICFlowMeter.csv`
- `Friday-02-03-2018_TrafficForML_CICFlowMeter.csv`
- `Thursday-01-03-2018_TrafficForML_CICFlowMeter.csv`

The larger `Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv` file was not downloaded in this first pass.

## Raw Audit

Verified raw audit:

- files: 5
- rows after removing repeated embedded headers: 4,525,400
- data hash: `414f7195ee1e137a`
- schema: 80 CICFlowMeter-style columns
- missing endpoint columns: `flow_id`, `src_ip`, `src_port`, `dst_ip`

Raw label counts:

| Label | Rows |
|---|---:|
| Benign | 3,764,269 |
| Bot | 286,191 |
| FTP-BruteForce | 193,360 |
| SSH-Bruteforce | 187,589 |
| Infilteration | 93,063 |
| Brute Force -Web | 611 |
| Brute Force -XSS | 230 |
| SQL Injection | 87 |

## Validation Sample

A real-data stratified sample was generated with:

- benign cap: 80,000
- attack cap per label: 30,000
- seed: 42
- rows: 200,928
- sample hash: `d90aca82728746b3`

Sample label counts:

| Label | Rows |
|---|---:|
| Benign | 80,000 |
| Bot | 30,000 |
| FTP-BruteForce | 30,000 |
| SSH-Bruteforce | 30,000 |
| Infilteration | 30,000 |
| Brute Force -Web | 611 |
| Brute Force -XSS | 230 |
| SQL Injection | 87 |

This sample is not synthetic. It is a capped subset of real CSE-CIC-IDS2018 rows.

## Binary Baseline

Command summary:

- models: LogisticRegression, HistGradientBoosting, RandomForest
- feature tier: `deployment_safe`
- seed: 42
- rows: 200,928
- completed runs: 12/12
- failed runs: 0
- skipped split: `endpoint_pair_holdout`, because the public CSV subset does not include endpoint IP columns

Macro-F1 by model and split:

| Model | Random | Temporal | Latest-day 2018-03-02 | Web holdout |
|---|---:|---:|---:|---:|
| LogisticRegression | 0.8618 | 0.6727 | 0.6604 | 0.6459 |
| HistGradientBoosting | 0.9224 | 0.8312 | 0.8204 | 0.7408 |
| RandomForest | 0.9158 | 0.9284 | 0.9195 | 0.7193 |

Interpretation:

- The random split is again optimistic for LogisticRegression and HistGradientBoosting.
- Web holdout degrades all three models, including RandomForest.
- RandomForest is unusually stable under temporal/latest-day holdout on this partial sample, so the manuscript should not overgeneralize the exact model ranking.

## Calibration Baselines

Calibration methods:

- raw probabilities
- Platt sigmoid
- isotonic regression

Rows: 24, failed rows: 0.

Key ECE values:

| Model | Split | Raw ECE | Platt ECE | Isotonic ECE |
|---|---|---:|---:|---:|
| LogisticRegression | random | 0.0395 | 0.0212 | 0.0040 |
| LogisticRegression | temporal | 0.3619 | 0.2038 | 0.1533 |
| LogisticRegression | latest-day | 0.3844 | 0.3287 | 0.3208 |
| LogisticRegression | Web holdout | 0.1693 | 0.2487 | 0.2309 |
| HistGradientBoosting | random | 0.0151 | 0.0188 | 0.0029 |
| HistGradientBoosting | temporal | 0.0864 | 0.1371 | 0.1310 |
| HistGradientBoosting | latest-day | 0.1416 | 0.1316 | 0.1380 |
| HistGradientBoosting | Web holdout | 0.1319 | 0.1215 | 0.1239 |

Interpretation:

- Calibration helps strongly under random split.
- Under stress splits, calibration is mixed: it improves some LogisticRegression temporal/latest-day errors but can degrade Web holdout or HGB temporal ECE.
- This supports reporting calibration as split-dependent, not as a universally reliable post-processing fix.

## Open-Set Baselines

Open-set run:

- sample size: 50,000 rows from the validation sample
- models: Isolation Forest, Local Outlier Factor
- unknown families: Web, Botnet, Infiltration, BruteForce
- completed runs: 8/8

AUROC for unknown-family scoring:

| Model | Web | Botnet | Infiltration | BruteForce |
|---|---:|---:|---:|---:|
| IsolationForest | 0.6526 | 0.4323 | 0.4742 | 0.7521 |
| LocalOutlierFactor | 0.8990 | 0.9574 | 0.6947 | 0.9087 |

Interpretation:

- LOF is much stronger than Isolation Forest on this partial sample for Web, Botnet and BruteForce unknown scoring.
- Isolation Forest performs poorly for Botnet and Infiltration in this setup.
- These results strengthen the paper by showing that open-set conclusions depend strongly on the anomaly baseline.

## Evidence Snapshot

Tracked artifacts:

`evidence/cse-cic-ids2018-partial-s42-001/`

Important files:

- `raw_audit_summary.json`
- `sample_summary.json`
- `sample_audit_summary.json`
- `cse_cic2018_partial_s42_results.csv`
- `cse_cic2018_calibration_partial_s42_results.csv`
- `cse_cic2018_open_set_partial_s42_results.csv`

## Limitations

- This is a partial CSE-CIC-IDS2018 validation using 5 of the available CSV files.
- The `Thuesday-20-02-2018` CSV was skipped initially because it is about 4.05 GB.
- The validation sample is stratified and capped, so class priors are not the original deployment priors.
- Endpoint-pair holdout is unavailable because these public processed CSVs do not include source/destination IP columns.
- Only seed 42 was run locally for the external validation sample.

## Manuscript Use

Use this result as:

> a partial external validation on real CSE-CIC-IDS2018 CICFlowMeter CSVs.

Do not present it as:

> full cross-dataset validation over the complete CSE-CIC-IDS2018 dataset.

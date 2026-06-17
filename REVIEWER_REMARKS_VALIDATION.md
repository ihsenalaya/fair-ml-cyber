# Reviewer Remarks Validation - FAIR-ML-CYBER

Date: 2026-06-17

This document validates the internal Q1 reviewer remarks one by one and translates them into concrete actions for the manuscript.

## Ethical Boundary

The article must not present generated, synthetic or RAG-created records as if they were real measured network traffic.

Acceptable uses:

- use a public documented second dataset and cite it;
- use RAG to retrieve documentation, schema descriptions and feature mappings;
- generate code, tables, mappings and experiment plans;
- generate synthetic data only for software unit tests, clearly labelled as synthetic and never reported as scientific evidence.

Not acceptable:

- generate artificial traffic records and hide their origin;
- report generated data as an external validation dataset;
- omit the source of any dataset used for results.

## Remark-by-Remark Validation

| # | Reviewer remark | Validation | Current evidence | Required action |
|---:|---|---|---|---|
| 1 | Single old CICIDS2017-like dataset is the main Q1 risk | Valid | Current paper uses one local CICIDS2017-like dataset; Q1 viability file already warns that single-dataset evidence is weak | Add a real public second dataset; cite source and describe differences |
| 2 | Advanced analyses are seed 42 only | Valid | `advanced-core-s42-001` has rare-class/multiclass/open-set/calibration/XAI only for seed 42 | Rerun advanced protocol on seeds 7 and 99 if budget permits; otherwise mark advanced results as seed-42 analysis |
| 3 | LR convergence is fixed only for seed 42 | Valid | `fullcore-lr2000-s42-001` has 0 convergence warnings; old seeds 7/99 still have max_iter=500 warnings | Run LR2000 jobs for seeds 7 and 99 before final LR multi-seed tables |
| 4 | Open-set analysis is too simple | Valid | Current open-set uses classifier uncertainty only | Add at least one anomaly/open-set baseline: Isolation Forest, One-Class SVM, autoencoder, energy score or conformal threshold |
| 5 | Calibration is measured but not corrected | Valid | ECE is reported, but no post-hoc calibration is compared | Add Platt/sigmoid calibration and isotonic regression; compare ECE/Brier before and after calibration |
| 6 | Explainability stability is too lightweight | Valid | HGB permutation importance uses sample size 2,000 and one repeat | Increase permutation repeats, add bootstrap/top-k stability confidence intervals |
| 7 | Rare-class results must be framed as failure analysis | Valid | Web rare classes have F1 0.0 in Web holdout despite nonzero support | Do not claim rare-class detection is solved; frame as evidence that aggregate metrics hide failure |
| 8 | Confidence intervals/statistical tests are missing | Valid | Tables report point estimates only | Add bootstrap CI for macro-F1, AUROC, AUPRC, ECE, and paired random-vs-stress comparisons |
| 9 | Endpoint-pair holdout is not discriminating enough | Valid | Endpoint-pair HGB CTS is near 1 in multi-seed results | Add service/port holdout if feasible; interpret endpoint-pair as a weaker stress-test |

## Decision

The reviewer remarks are mostly valid. The strongest path to a Q1-ready manuscript is:

1. Add a real second dataset.
2. Rerun convergence-clean LR for seeds 7 and 99.
3. Repeat the advanced protocol on additional seeds if compute budget permits.
4. Add calibration and open-set baselines.
5. Add confidence intervals and statistical tests.

## Second Dataset Requirement

The second dataset should satisfy three constraints:

- public and citable;
- downloadable in CSV or flow format;
- compatible enough with the current flow-based pipeline to avoid turning the paper into a separate data-engineering project.

Recommended primary candidate: **CIC-UNSW-NB15 Augmented Dataset** from the Canadian Institute for Cybersecurity / UNB.

Reason:

- it is based on UNSW-NB15, so it is not the same underlying scenario as CICIDS2017;
- it uses CICFlowMeter extraction, making it closer to the current feature representation;
- the official page lists the files `CICFlowMeter_out.csv`, `Data.csv`, `Label.csv` and `Readme.txt`;
- it supports a clean cross-dataset/second-dataset validation without fabricating data.

Backup candidates:

- CSE-CIC-IDS2018: closest feature compatibility, but same CIC/UNB family and potentially too close to CICIDS2017-like data;
- UNSW-NB15 original: strong external dataset, but requires more schema adaptation;
- TON_IoT: stronger domain shift, but much more schema/domain adaptation;
- UQ NetFlow collections: best for standardized NetFlow cross-dataset work, but requires building a separate NetFlow mapping layer.


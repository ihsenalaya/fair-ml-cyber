# UNSW-NB15 Access Attempt

Date: 2026-06-17

## Summary

UNSW-NB15 is free for academic research use, but the official automated download was blocked in this environment. No fabricated identity data was used, and no third-party mirror was silently treated as official data.

Tracked evidence:

`evidence/unsw-nb15-access-attempt-2026-06-17/`

## Official UNSW-NB15 Source

Official page:

https://research.unsw.edu.au/projects/unsw-nb15-dataset

The page states that:

- the source files include pcap, BRO, Argus, CSV files and reports;
- the dataset has 2,540,044 records in four CSV files: `UNSW-NB15_1.csv`, `UNSW-NB15_2.csv`, `UNSW-NB15_3.csv`, `UNSW-NB15_4.csv`;
- additional files include `UNSW-NB15_GT.csv`, `UNSW-NB15_LIST_EVENTS.csv`, `UNSW_NB15_training-set.csv`, and `UNSW_NB15_testing-set.csv`;
- academic research use is granted, with citation requirements.

However, the official download link redirects to a UNSW SharePoint folder. Direct access returned `403 Forbidden` with `X-Forms_Based_Auth_Required`, so the files could not be downloaded from the command line without an authenticated session.

## Official CIC-UNSW-NB15 Source

Official page:

https://www.unb.ca/cic/datasets/cic-unsw-nb15.html

The UNB page states that CIC-UNSW-NB15 was generated from UNSW-NB15 traffic using CICFlowMeter and lists four files:

- `CICFlowMeter_out.csv`
- `Data.csv`
- `Label.csv`
- `Readme.txt`

The download link opens:

https://cicresearch.ca//CICDataset/CIC-UNSW/

This page requests personal information and currently displays `Server error. Please try again later.` No automated form submission was attempted.

## Decision

For the current Q1 repair, the completed free external validation is CSE-CIC-IDS2018:

- all 10 public processed CSV files downloaded;
- 16,232,943 raw rows audited;
- 363,648-row real stratified sample built;
- seed 42 binary protocol run with LR, HGB and RF;
- evidence in `evidence/cse-cic-ids2018-full-sample-s42-001/`.

UNSW-NB15 remains a legitimate-access follow-up, not a completed dataset in this repo.

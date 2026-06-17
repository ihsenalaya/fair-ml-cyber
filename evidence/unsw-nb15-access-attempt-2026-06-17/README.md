# UNSW-NB15 Access Attempt - 2026-06-17

This evidence note records why no official UNSW-NB15 or CIC-UNSW-NB15 CSV files were downloaded automatically in this run.

Official sources checked:

- UNSW-NB15 official UNSW page: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- CIC-UNSW-NB15 official UNB page: https://www.unb.ca/cic/datasets/cic-unsw-nb15.html
- CIC-UNSW download form: https://cicresearch.ca//CICDataset/CIC-UNSW/

Findings:

- The UNSW page states that UNSW-NB15 is free for academic research use, lists the four original CSV files, the ground-truth/event files, and the predefined train/test CSVs.
- The official UNSW download link redirects to SharePoint. Direct command-line access returned `403 Forbidden` with `X-Forms_Based_Auth_Required`, so the file listing could not be downloaded without an authenticated browser/session.
- The CIC-UNSW-NB15 page lists the augmented dataset files (`CICFlowMeter_out.csv`, `Data.csv`, `Label.csv`, `Readme.txt`) and provides a download link.
- The CIC-UNSW download link opens a form requesting personal information and currently displays `Server error. Please try again later.` No automated form submission was attempted, and no invented identity data was used.

Methodological decision:

- Do not use unverified third-party mirrors as official UNSW-NB15 evidence unless explicitly labelled as mirrors.
- Use the completed CSE-CIC-IDS2018 validation as the current free external dataset evidence.
- Keep UNSW-NB15/CIC-UNSW-NB15 open as a legitimate-access follow-up, not as a fabricated or silently mirrored dataset.

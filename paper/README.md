# FAIR-ML-CYBER Paper Draft

This directory contains the LaTeX manuscript draft for internal review.

## Files

- `main.tex`: journal-style manuscript source.
- `main.pdf`: compiled PDF review copy generated with `tectonic`.

## Build

From this directory:

```bash
tectonic main.tex
```

The bibliography is read from `../references.bib`.

## Status

This is a review draft, not a final submission package. It uses only verified results from the tracked experiment reports and evidence snapshots. The main limitations still to address before a Q1 submission are:

- advanced analyses are seed 42 only;
- LR2000 convergence-clean reruns are still needed for seeds 7 and 99 if final LR multi-seed tables are used;
- open-set and calibration baselines should be strengthened;
- confidence intervals/statistical tests are not yet included.

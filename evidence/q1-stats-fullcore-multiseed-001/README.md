# Q1 Full-Core Multi-Seed Statistics Evidence

Date: 2026-06-17

This snapshot contains robust statistical summaries generated from the verified full-data core result CSVs:

- `evidence/fullcore-mem-s42-001/fullcore_mem_s42_results.csv`
- `evidence/fullcore-mem-s7-001/fullcore_mem_s7_results.csv`
- `evidence/fullcore-mem-s99-001/fullcore_mem_s99_results.csv`

Scope:

- metric: `macro_f1`
- completed rows: 60
- paired units for random-vs-stress comparisons: seed x feature tier, giving 6 pairs per model
- bootstrap iterations: 5000
- confidence level: 95%

Important limitation: bootstrap intervals are over available experimental units, not over individual flow-level predictions. They quantify robustness across seeds and feature tiers, not per-flow uncertainty.

Files:

- `q1_metric_summary.csv`: bootstrap mean/std/95% CI by model, feature tier and split
- `q1_paired_split_comparisons.csv`: paired random-vs-stress deltas, ratios, exact sign-flip p-values and effect sizes
- `q1_inter_seed_variance.csv`: variance across seeds by model, feature tier and split
- `q1_statistics_report.md`: human-readable summary
- `q1_statistics_summary.json`: command metadata

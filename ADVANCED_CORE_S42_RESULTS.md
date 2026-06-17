# Advanced Full-Data Results - `advanced-core-s42-001`

This report summarizes the verified full-data advanced analyses requested after the core binary runs: rare-class, multiclass, open-set, calibration/abstention and explanation stability.

No result below is inferred from memory. All values come from downloaded Azure ML artifacts under:

`data/azure_jobs/advanced-core-s42-001/named-outputs/work_dir/advanced_results/`

Tracked evidence snapshot:

`evidence/advanced-core-s42-001/`

## Run Definition

| Item | Value |
|---|---|
| Azure ML job | `advanced-core-s42-001` |
| YAML | `azureml/advanced_core_seed42_job.yml` |
| Git commit used by Azure ML | `0fb637fc8bb343aacb22731b9c625683f032bb68` |
| Git dirty flag | `False` |
| Compute | `cpu-memory-cluster`, `Standard_E8ds_v5`, 1 instance |
| Dataset | `fair_ml_cyber_csvs:1` |
| Rows | 2,438,052 |
| Seed | 42 |
| Feature tier | `deployment_safe` |
| Models | `logistic_regression`, `hist_gradient_boosting` |
| Splits | `random_stratified`, `temporal`, `latest_day_holdout`, `scenario_holdout_Web`, `endpoint_pair_holdout` |
| Unknown families | `Web`, `Botnet`, `PortScan`, `DDoS` |
| Explanation config | sample size 2,000; permutation repeats 1 |

## Operational Record

| Step | Duration | Result |
|---|---:|---|
| Submit | 3:14.50 wall clock | Submitted, initial status `Starting` |
| Stream | 1:52:51 wall clock | Completed, exit status 0 |
| Download | 3:22.52 wall clock | Artifacts downloaded |
| Local summary | Not timed | CSV artifacts read and summarized locally |

The run completed:

- 10 binary runs;
- 10 multiclass runs;
- 8 open-set runs;
- 0 skipped splits.

## Binary Results and Calibration

| Model | Split | Macro-F1 | AUROC | AUPRC | ECE | Brier |
|---|---|---:|---:|---:|---:|---:|
| HGB | `random_stratified` | 0.9960 | 0.9999 | 0.9998 | 0.0009 | 0.0023 |
| LR | `random_stratified` | 0.9370 | 0.9895 | 0.9695 | 0.0345 | 0.0393 |
| HGB | `temporal` | 0.2296 | 0.7540 | 0.8639 | 0.7013 | 0.7006 |
| LR | `temporal` | 0.5395 | 0.9665 | 0.9825 | 0.3955 | 0.3497 |
| HGB | `day_holdout_2017-07-07` | 0.3678 | 0.8972 | 0.8002 | 0.4180 | 0.4175 |
| LR | `day_holdout_2017-07-07` | 0.6370 | 0.9231 | 0.8733 | 0.2528 | 0.2338 |
| HGB | `scenario_holdout_Web` | 0.6218 | 0.9350 | 0.2798 | 0.0093 | 0.0094 |
| LR | `scenario_holdout_Web` | 0.4833 | 0.8666 | 0.0399 | 0.0661 | 0.0518 |
| HGB | `endpoint_pair_holdout` | 0.9917 | 0.9999 | 0.9993 | 0.0020 | 0.0028 |
| LR | `endpoint_pair_holdout` | 0.8837 | 0.9846 | 0.8432 | 0.0584 | 0.0466 |

Key verified observation: temporal and day-holdout shifts are not only lower-performing; they are poorly calibrated. HGB temporal ECE is 0.7013 and LR temporal ECE is 0.3955.

Binary warning checks:

- total `warning_count`: 0;
- total `convergence_warning_count`: 0.

## Multiclass Results

| Model | Split | Macro-F1 | Weighted-F1 |
|---|---|---:|---:|
| HGB | `random_stratified` | 0.7479 | 0.9901 |
| LR | `random_stratified` | 0.4487 | 0.9175 |
| HGB | `temporal` | 0.0415 | 0.1360 |
| LR | `temporal` | 0.0453 | 0.1621 |
| HGB | `day_holdout_2017-07-07` | 0.0523 | 0.4256 |
| LR | `day_holdout_2017-07-07` | 0.0546 | 0.4439 |
| HGB | `scenario_holdout_Web` | 0.0762 | 0.9791 |
| LR | `scenario_holdout_Web` | 0.0667 | 0.9225 |
| HGB | `endpoint_pair_holdout` | 0.4447 | 0.9923 |
| LR | `endpoint_pair_holdout` | 0.3044 | 0.9051 |

Key verified observation: weighted-F1 can remain high while macro-F1 collapses, especially for scenario/Web and endpoint-pair splits. This supports reporting macro-F1 and per-class behavior rather than relying on aggregate weighted metrics.

Multiclass warning checks:

- total `warning_count`: 0;
- total `convergence_warning_count`: 0;
- Azure log has 16 sklearn `UserWarning: y_pred contains classes not in y_true` messages during shifted multiclass/per-class evaluation.

## Rare-Class Results

Rare labels present in the advanced artifact:

- `Heartbleed`;
- `Web_Brute_Force`;
- `Web_SQL_Injection`;
- `Web_XSS`.

Best observed rare-class F1 values:

| Label | Best split/model | Support | F1 |
|---|---|---:|---:|
| `Heartbleed` | `random_stratified` / LR | 2 | 0.0003 |
| `Web_Brute_Force` | `random_stratified` / HGB | 410 | 0.8671 |
| `Web_SQL_Injection` | `endpoint_pair_holdout` / LR | 2 | 0.0016 |
| `Web_XSS` | `random_stratified` / HGB | 203 | 0.6929 |

Shifted rare-class behavior is weak. For `scenario_holdout_Web`, all reported Web rare-class F1 values are 0.0 despite nonzero supports:

| Label | Support | LR F1 | HGB F1 |
|---|---:|---:|---:|
| `Web_Brute_Force` | 2,734 | 0.0000 | 0.0000 |
| `Web_SQL_Injection` | 24 | 0.0000 | 0.0000 |
| `Web_XSS` | 1,358 | 0.0000 | 0.0000 |

This is a strong argument for rare-class and scenario-aware evaluation. It also means rare-class claims must be framed as failure analysis, not as a solved detection result.

## Open-Set Results

The open-set protocol holds out one attack family from training and evaluates whether uncertainty can identify the unknown family.

| Unknown family | Model | Unknown support | Uncertainty AUROC | Uncertainty AUPRC | Attack recall as attack | Unknown recall at p90 uncertainty |
|---|---|---:|---:|---:|---:|---:|
| `Web` | LR | 4,116 | 0.8697 | 0.0407 | 0.0168 | 0.0649 |
| `Web` | HGB | 4,116 | 0.9353 | 0.3926 | 0.1761 | 0.6618 |
| `Botnet` | LR | 5,508 | 0.7607 | 0.0286 | 0.7108 | 0.0005 |
| `Botnet` | HGB | 5,508 | 0.9262 | 0.2953 | 0.3838 | 0.6899 |
| `PortScan` | LR | 161,323 | 0.9501 | 0.7690 | 0.4963 | 0.2348 |
| `PortScan` | HGB | 161,323 | 0.9954 | 0.9882 | 0.6192 | 0.4393 |
| `DDoS` | LR | 95,733 | 0.2019 | 0.1517 | 0.9650 | 0.0545 |
| `DDoS` | HGB | 95,733 | 0.9587 | 0.7223 | 0.0000 | 0.3570 |

Key verified observation: uncertainty-based open-set behavior is model- and family-dependent. HGB uncertainty ranks unknowns well for all four families, while LR fails badly for DDoS uncertainty ranking despite high binary attack recall.

## Abstention Results

At approximately 90% coverage, selective macro-F1 remains poor on the hard shifts:

| Model | Split | Actual coverage | Review rate | Selective macro-F1 | Accepted attack recall |
|---|---|---:|---:|---:|---:|
| HGB | `temporal` | 0.9029 | 0.0971 | 0.2416 | 0.0000 |
| LR | `temporal` | 0.9000 | 0.1000 | 0.5931 | 0.3975 |
| HGB | `day_holdout_2017-07-07` | 0.9001 | 0.0999 | 0.3867 | 0.0000 |
| LR | `day_holdout_2017-07-07` | 0.9000 | 0.1000 | 0.6940 | 0.4078 |
| HGB | `scenario_holdout_Web` | 0.9014 | 0.0986 | 0.4994 | 0.0010 |
| LR | `scenario_holdout_Web` | 0.9000 | 0.1000 | 0.4960 | 0.0094 |

At 50% coverage, LR selective macro-F1 improves strongly for temporal/day-holdout, but this means half of the flows are sent to review. This should be framed as a coverage-risk tradeoff, not a direct model improvement.

## Explanation Stability

Top-15 feature-overlap Jaccard versus `random_stratified`:

| Model | Target split | Jaccard | Overlap count |
|---|---|---:|---:|
| HGB | `temporal` | 0.0714 | 2 |
| HGB | `day_holdout_2017-07-07` | 0.1538 | 4 |
| HGB | `scenario_holdout_Web` | 0.1538 | 4 |
| HGB | `endpoint_pair_holdout` | 0.5000 | 10 |
| LR | `temporal` | 0.5789 | 11 |
| LR | `day_holdout_2017-07-07` | 0.6667 | 12 |
| LR | `scenario_holdout_Web` | 0.5789 | 11 |
| LR | `endpoint_pair_holdout` | 0.7647 | 13 |

Key verified observation: HGB explanations are much less stable across the hardest shifts than LR explanations. This supports an article contribution around explanation stability under deployment shifts.

## Limitations and Warnings

- This advanced run is seed 42 only. It is sufficient to establish feasibility and produce article-quality analyses, but final robustness claims should be repeated on seeds 7 and 99 if compute budget allows.
- HGB permutation importance used sample size 2,000 and one permutation repeat. This is a lightweight stability probe, not a final high-precision explanation study.
- The 16 sklearn `y_pred contains classes not in y_true` warnings are methodologically important. They indicate shifted multiclass label support and should be discussed rather than hidden.
- A pandas `FutureWarning` appeared during feature-importance concatenation. It did not stop artifact creation, but the code should be made future-proof before final archival release.
- A local summary script initially looked for `brier` instead of the actual column `brier_score`; this was corrected and does not affect Azure artifacts.

## Manuscript Implication

This run materially strengthens the Q1-level angle:

1. Random binary performance is high, but temporal/day/scenario shifts expose poor transferability.
2. Calibration degrades sharply under the same shifts.
3. Multiclass and rare-class results are far weaker than binary results, especially under Web holdout.
4. Open-set detection is not uniformly solved by uncertainty; behavior depends on family and model.
5. Explanation stability differs strongly by model and split.

The article should therefore be framed as a rigorous deployment-reliability and benchmark-validity study, not as a paper claiming a new detector with universally superior accuracy.

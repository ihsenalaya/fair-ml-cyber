# Full-Data Core Results - `fullcore-mem-s42-001`

This file summarizes verified outputs from the Azure ML full-data core run. These results are valid empirical evidence for the current binary-classification core protocol, but they are not yet a complete Q1 paper package: repeated seeds, rare-class/multi-class analysis, open-set tests, calibration/abstention analysis and explanation stability are still required.

For the current multi-seed comparison, see `FULLCORE_MEM_MULTI_SEED_RESULTS.md`.

## Run Scope

| Item | Value |
|---|---|
| Azure ML job | `fullcore-mem-s42-001` |
| Commit | `0a4808be5f5f5edf487767eb2496b3591c5ab98b` |
| Git dirty flag | `False` in the job creation metadata |
| Compute | Azure ML `cpu-memory-cluster`, `Standard_E8ds_v5`, 1 instance |
| Environment | `fair-ml-cyber-runtime-env:1` with runtime pip install |
| Command | `fair_ml_cyber.cli run-experiment --seed 42 --models logistic_regression hist_gradient_boosting --feature-tiers no_identity deployment_safe --splits random_stratified temporal latest_day_holdout scenario_holdout_Web endpoint_pair_holdout --result-prefix fullcore_mem_s42 --no-save-models --no-save-prepared` |
| Full dataset audit | 18 CSV files, 2,438,052 rows, dataset hash `f51899df9bd60758` |
| Sample size | Full dataset, 2,438,052 rows, run data hash `171746c8753403c4` |
| Models | `logistic_regression`, `hist_gradient_boosting` |
| Feature tiers | `no_identity` with 117 features, `deployment_safe` with 115 features |
| Splits | `random_stratified`, `temporal`, `day_holdout_2017-07-07`, `scenario_holdout_Web`, `endpoint_pair_holdout` |
| Run matrix | 20 combinations, 20 completed, 0 failed, 0 skipped |
| Local artifact root | `data/azure_jobs/fullcore-mem-s42-001` |
| Result CSV | `data/azure_jobs/fullcore-mem-s42-001/named-outputs/work_dir/results/fullcore_mem_s42_results.csv` |
| Summary JSON | `data/azure_jobs/fullcore-mem-s42-001/named-outputs/work_dir/results/fullcore_mem_s42_summary.json` |
| Event log | `data/azure_jobs/fullcore-mem-s42-001/named-outputs/work_dir/results/fullcore_mem_s42_events.jsonl` |
| Tracked evidence snapshot | `evidence/fullcore-mem-s42-001/` |

## Timings And Resources

| Step | Duration | CLI max RSS | Result |
|---|---:|---:|---|
| Memory compute creation | 2:49.42 wall clock | 210,176 KB | `cpu-memory-cluster` created successfully |
| Job submission | 3:08.31 wall clock | 223,380 KB | Submitted; initial status `Starting` |
| Azure stream command | 43:42.95 wall clock | 209,540 KB | Exit status 0 |
| Experiment engine window | 2026-06-17 00:50:41 UTC to 01:29:40 UTC | Not separately measured | 20/20 runs completed |
| Artifact download | 3:04.15 wall clock | 214,884 KB | Exit status 0 |
| Local artifact size | 3.4 MB | N/A | Downloaded successfully |

The earlier `fullcore-s42-001` run on `Standard_DS3_v2` failed with Azure ML reporting the Python process killed by `SIGKILL`, likely out of memory. The `Standard_E8ds_v5` rerun completed the same core protocol successfully.

The Azure CLI `az ml job show` command timed out after 120 seconds after completion, so final status is evidenced by `az ml job stream` exit status 0 and downloaded artifacts, not by `az ml job show`.

## Overall Metrics

Across all 20 full-data combinations:

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| macro-F1 | 0.664466 | 0.267484 | 0.229624 | 0.999539 |
| balanced accuracy | 0.725142 | 0.219524 | 0.476562 | 0.999640 |
| AUROC | 0.929869 | 0.076038 | 0.753987 | 0.999998 |
| AUPRC | 0.771429 | 0.311301 | 0.039886 | 0.999995 |
| MCC | 0.460766 | 0.406679 | -0.020457 | 0.999079 |
| train seconds | 108.649122 | 46.914613 | 48.743103 | 181.691925 |
| inference seconds | 2.008685 | 1.062232 | 0.745990 | 4.888859 |

Total training time across the 20 model/split/tier combinations was 2,172.982 seconds. Total recorded inference time was 40.174 seconds.

## Macro-F1 By Split

Values are averaged across the two feature tiers.

| Split | HistGradientBoosting | LogisticRegression |
|---|---:|---:|
| `random_stratified` | 0.9978 | 0.9364 |
| `endpoint_pair_holdout` | 0.9955 | 0.8859 |
| `temporal` | 0.2316 | 0.5401 |
| `day_holdout_2017-07-07` | 0.3698 | 0.6388 |
| `scenario_holdout_Web` | 0.5653 | 0.4836 |

## Macro-F1 By Feature Tier And Split

| Feature tier | Split | HistGradientBoosting | LogisticRegression |
|---|---|---:|---:|
| `deployment_safe` | `random_stratified` | 0.9960 | 0.9370 |
| `deployment_safe` | `temporal` | 0.2296 | 0.5399 |
| `deployment_safe` | `day_holdout_2017-07-07` | 0.3678 | 0.6376 |
| `deployment_safe` | `scenario_holdout_Web` | 0.6218 | 0.4833 |
| `deployment_safe` | `endpoint_pair_holdout` | 0.9917 | 0.8837 |
| `no_identity` | `random_stratified` | 0.9995 | 0.9357 |
| `no_identity` | `temporal` | 0.2336 | 0.5402 |
| `no_identity` | `day_holdout_2017-07-07` | 0.3717 | 0.6399 |
| `no_identity` | `scenario_holdout_Web` | 0.5088 | 0.4840 |
| `no_identity` | `endpoint_pair_holdout` | 0.9992 | 0.8881 |

## AUPRC By Feature Tier And Split

| Feature tier | Split | HistGradientBoosting | LogisticRegression |
|---|---|---:|---:|
| `deployment_safe` | `random_stratified` | 0.9998 | 0.9695 |
| `deployment_safe` | `temporal` | 0.8639 | 0.9832 |
| `deployment_safe` | `day_holdout_2017-07-07` | 0.8002 | 0.8707 |
| `deployment_safe` | `scenario_holdout_Web` | 0.2798 | 0.0399 |
| `deployment_safe` | `endpoint_pair_holdout` | 0.9993 | 0.8432 |
| `no_identity` | `random_stratified` | 1.0000 | 0.9699 |
| `no_identity` | `temporal` | 0.8773 | 0.9820 |
| `no_identity` | `day_holdout_2017-07-07` | 0.7384 | 0.8772 |
| `no_identity` | `scenario_holdout_Web` | 0.4534 | 0.0405 |
| `no_identity` | `endpoint_pair_holdout` | 1.0000 | 0.8404 |

## Cyber Transferability Score

`CTS_macro_F1 = macro_F1_stress_split / macro_F1_random_stratified` for the same model and feature tier.

| Feature tier | Target split | HistGradientBoosting | LogisticRegression |
|---|---|---:|---:|
| `deployment_safe` | `temporal` | 0.2305 | 0.5762 |
| `deployment_safe` | `day_holdout_2017-07-07` | 0.3693 | 0.6805 |
| `deployment_safe` | `scenario_holdout_Web` | 0.6242 | 0.5158 |
| `deployment_safe` | `endpoint_pair_holdout` | 0.9957 | 0.9430 |
| `no_identity` | `temporal` | 0.2337 | 0.5773 |
| `no_identity` | `day_holdout_2017-07-07` | 0.3719 | 0.6839 |
| `no_identity` | `scenario_holdout_Web` | 0.5090 | 0.5172 |
| `no_identity` | `endpoint_pair_holdout` | 0.9997 | 0.9491 |

## Interpretation For The Article

The full-data run strongly supports the article's central claim: random stratified evaluation is optimistic and does not predict deployment-style robustness. HistGradientBoosting reaches almost perfect macro-F1 under random and endpoint-pair holdout, but drops sharply under temporal and day-holdout evaluation. Logistic Regression is weaker than HistGradientBoosting under random split, but is more stable on temporal and day-holdout splits.

This finding is scientifically useful because it changes the model ranking depending on the evaluation protocol. The paper should frame this as an evaluation-validity and transferability contribution, not as a new state-of-the-art classifier claim.

The Web scenario holdout also shows why AUPRC must be reported carefully: Logistic Regression has macro-F1 near 0.48 but AUPRC around 0.04 for the Web holdout, consistent with a very low positive rate in the test split. This must be discussed rather than hidden.

## Operational Issues Observed

| Issue | Status | Impact |
|---|---|---|
| `Standard_DS3_v2` full-data run killed by `SIGKILL` | Resolved by memory rerun | `Standard_DS3_v2` is not sufficient for the full-data core protocol |
| Two `ConvergenceWarning` messages for Logistic Regression | Open methodological issue | Some LR full-data fits reached `max_iter=500`; final protocol should either tune solver/iterations or report the warning as a limitation |
| `az ml job show` timed out after 120 s | Open Azure CLI observation | Use stream exit status and downloaded artifacts as evidence |
| Runtime pip install in Azure container | Accepted workaround | Adds startup overhead because image build through ACR was avoided |
| System storage logs include transient blob HEAD 404 warnings | Observed, non-fatal | The job completed and artifacts downloaded; treat as Azure storage synchronization noise unless repeated failures appear |

## Remaining Work Before A Q1 Manuscript

The current full-data core result is a strong foundation, but the manuscript should not stop here. Required next steps:

- repeat the core protocol with additional seeds where randomness affects splits/models;
- add Random Forest or another tree baseline only if compute/memory cost is controlled;
- run rare-class and multi-class analyses instead of relying only on binary metrics;
- implement open-set family holdout;
- add calibration, abstention and coverage-risk curves;
- add explanation-stability analysis;
- convert the verified results into LaTeX tables and figures only after these missing experiments are complete.

# LogisticRegression Convergence Rerun - `fullcore-lr2000-s42-001`

This note documents the full-data LogisticRegression rerun used to address the convergence warnings observed in the earlier `max_iter=500` core runs.

## Run Definition

| Item | Value |
|---|---|
| Azure ML job | `fullcore-lr2000-s42-001` |
| YAML | `azureml/full_core_lr2000_seed42_job.yml` |
| Git commit | `0fb637fc8bb343aacb22731b9c625683f032bb68` |
| Git dirty flag | `False` |
| Compute | `cpu-memory-cluster`, `Standard_E8ds_v5`, 1 instance |
| Dataset | `fair_ml_cyber_csvs:1` |
| Rows | 2,438,052 |
| Seed | 42 |
| Model | `logistic_regression` |
| Feature tiers | `no_identity`, `deployment_safe` |
| Splits | `random_stratified`, `temporal`, `latest_day_holdout`, `scenario_holdout_Web`, `endpoint_pair_holdout` |
| LR configuration change | `max_iter=2000` instead of the previous `max_iter=500` |

## Operational Record

| Step | Command summary | Duration | Result |
|---|---|---:|---|
| Submit | `az ml job create ... --file full_core_lr2000_seed42_job.yml --name fullcore-lr2000-s42-001` | 4:28.82 wall clock | Submitted, initial status `Starting` |
| Stream | `az ml job stream ... --name fullcore-lr2000-s42-001` | 29:27.58 wall clock | Completed, exit status 0 |
| Download | `az ml job download ... --name fullcore-lr2000-s42-001 --all` | 2:50.39 wall clock | Artifacts downloaded |
| Local summary | `pandas.read_csv(...)` over downloaded `results.csv` | Not timed | 10 rows, all completed |

Tracked evidence snapshot:

`evidence/fullcore-lr2000-s42-001/`

## Results

| Feature tier | Split | Macro-F1 | AUROC | Train seconds | Inference seconds | Conv. warnings |
|---|---|---:|---:|---:|---:|---:|
| `deployment_safe` | `day_holdout_2017-07-07` | 0.637011 | 0.923075 | 169.465770 | 1.817316 | 0 |
| `deployment_safe` | `endpoint_pair_holdout` | 0.883657 | 0.984554 | 148.137877 | 0.739531 | 0 |
| `deployment_safe` | `random_stratified` | 0.937020 | 0.989477 | 113.152722 | 1.070863 | 0 |
| `deployment_safe` | `scenario_holdout_Web` | 0.483318 | 0.866589 | 158.106251 | 1.092722 | 0 |
| `deployment_safe` | `temporal` | 0.539465 | 0.966546 | 188.011737 | 1.133561 | 0 |
| `no_identity` | `day_holdout_2017-07-07` | 0.639923 | 0.924553 | 141.418819 | 1.943945 | 0 |
| `no_identity` | `endpoint_pair_holdout` | 0.888098 | 0.983105 | 129.037311 | 0.771288 | 0 |
| `no_identity` | `random_stratified` | 0.935718 | 0.989533 | 132.739334 | 1.014906 | 0 |
| `no_identity` | `scenario_holdout_Web` | 0.483978 | 0.869121 | 158.488482 | 1.039421 | 0 |
| `no_identity` | `temporal` | 0.540205 | 0.965045 | 163.305619 | 1.028162 | 0 |

Aggregate checks from the downloaded CSV:

- rows: 10;
- completed rows: 10;
- failed rows: 0;
- total `warning_count`: 0;
- maximum `warning_count`: 0;
- total `convergence_warning_count`: 0;
- maximum `convergence_warning_count`: 0;
- total LR training time recorded by the experiment engine: 1,501.864 seconds.

## Interpretation

For seed 42, the LogisticRegression convergence issue is resolved by increasing `max_iter` to 2000. The rerun should replace the earlier seed 42 LR rows in final LR-specific tables if the manuscript reports convergence-clean LR results.

The older `fullcore-mem-s7-001` and `fullcore-mem-s99-001` runs still contain their original `max_iter=500` convergence warnings. If the final manuscript needs convergence-clean multi-seed LR statistics, the same LR2000 rerun should also be executed for seeds 7 and 99.

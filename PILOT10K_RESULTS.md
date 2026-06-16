# Pilot Experiment Results - `pilot10k-001`

This file summarizes verified outputs from the Azure ML pilot run. It is evidence for pipeline stability and experimental design, not final paper evidence.

## Run Scope

| Item | Value |
|---|---|
| Azure ML job | `pilot10k-001` |
| Commit | `6c4c9949b2c4060d485ef546c5a956c55352d14c` |
| Git dirty flag | `False` in the job creation metadata |
| Compute | Azure ML `cpu-cluster`, `Standard_DS3_v2`, 1 instance |
| Environment | `fair-ml-cyber-runtime-env:1` with runtime pip install |
| Command | `fair_ml_cyber.cli run-experiment --sample-per-file 10000 --seed 42 --result-prefix pilot10k` |
| Full dataset audit | 18 CSV files, 2,438,052 rows, dataset hash `f51899df9bd60758` |
| Pilot sample | 125,517 rows, sample data hash `7ca87e5ece4acd51` |
| Models | `logistic_regression`, `random_forest`, `hist_gradient_boosting` |
| Feature tiers | `no_identity` with 117 features, `deployment_safe` with 115 features |
| Splits | `random_stratified`, `temporal`, `day_holdout_2017-07-07`, `scenario_holdout_Web`, `endpoint_pair_holdout` |
| Run matrix | 30 combinations, 30 completed, 0 failed |
| Local artifact root | `data/azure_jobs/pilot10k-001` |

## Timings And Resources

| Step | Duration | CLI max RSS | Result |
|---|---:|---:|---|
| Job submission | 3:22.49 wall clock | 222,828 KB | Submitted; initial status `Starting` |
| Azure stream command | 12:17.98 wall clock | 210,624 KB | Exit status 0 |
| Experiment engine window | 2026-06-16 21:54:28 UTC to 22:00:10 UTC | Not separately measured | 30/30 runs completed |
| Artifact download | 5:20.79 wall clock | 287,096 KB | Exit status 0 |
| Local artifact size | 205 MB | N/A | Downloaded successfully |

The Azure CLI `az ml job show` command timed out after 120 seconds after the run completed, so the final status is evidenced by `az ml job stream` exit status 0 and downloaded artifacts, not by `az ml job show`.

## Overall Metrics

Across all 30 pilot combinations:

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| macro-F1 | 0.636333 | 0.336720 | 0.130500 | 0.999058 |
| balanced accuracy | 0.743680 | 0.224708 | 0.494717 | 0.999002 |
| AUROC | 0.948611 | 0.056088 | 0.775810 | 0.999990 |
| AUPRC | 0.920074 | 0.124465 | 0.591295 | 0.999993 |
| MCC | 0.485259 | 0.432126 | -0.024850 | 0.998116 |
| train seconds | 7.011019 | 2.030675 | 4.079282 | 10.809332 |
| inference seconds | 0.153041 | 0.084464 | 0.041087 | 0.376720 |

## Macro-F1 By Split

Values are averaged across the two feature tiers.

| Split | HistGradientBoosting | LogisticRegression | RandomForest |
|---|---:|---:|---:|
| `random_stratified` | 0.9974 | 0.9313 | 0.9970 |
| `endpoint_pair_holdout` | 0.9959 | 0.9320 | 0.9948 |
| `temporal` | 0.1325 | 0.7860 | 0.1308 |
| `day_holdout_2017-07-07` | 0.2330 | 0.7034 | 0.2204 |
| `scenario_holdout_Web` | 0.6007 | 0.4735 | 0.4163 |

## Macro-F1 By Feature Tier And Split

| Feature tier | Split | HistGradientBoosting | LogisticRegression | RandomForest |
|---|---|---:|---:|---:|
| `deployment_safe` | `random_stratified` | 0.9958 | 0.9314 | 0.9957 |
| `deployment_safe` | `temporal` | 0.1321 | 0.7857 | 0.1305 |
| `deployment_safe` | `day_holdout_2017-07-07` | 0.2205 | 0.7033 | 0.2202 |
| `deployment_safe` | `scenario_holdout_Web` | 0.5494 | 0.4610 | 0.4155 |
| `deployment_safe` | `endpoint_pair_holdout` | 0.9938 | 0.9195 | 0.9927 |
| `no_identity` | `random_stratified` | 0.9991 | 0.9311 | 0.9983 |
| `no_identity` | `temporal` | 0.1329 | 0.7863 | 0.1312 |
| `no_identity` | `day_holdout_2017-07-07` | 0.2455 | 0.7035 | 0.2205 |
| `no_identity` | `scenario_holdout_Web` | 0.6519 | 0.4859 | 0.4171 |
| `no_identity` | `endpoint_pair_holdout` | 0.9980 | 0.9444 | 0.9969 |

## Interpretation For The Article

The pilot supports the core article direction: random splits substantially overstate deployment robustness, while temporal, day-holdout and scenario-holdout protocols expose sharp transferability failures. This is a useful Q1-oriented research angle because it focuses on evaluation validity, feature safety and deployment transfer rather than only reporting another high IDS accuracy table.

This pilot must not be used as final scientific evidence because it uses a 10,000-row-per-file sample and only one seed. Final experiments should run larger or full-data protocols, record repeated seeds where stochastic splitting is used, and keep the same strict separation between debug/pilot/final evidence.

## Operational Issues Observed

| Issue | Status | Impact |
|---|---|---|
| Runtime pip install in Azure container | Expected workaround | Adds startup overhead because image build through ACR was avoided |
| pip root-user warnings | Observed | Benign in Azure container context, but should be recorded |
| `az ml job show` timeout after 120 s | Open observation | Do not use it as evidence for this job |
| `az ml job download --all` large-file warnings | Closed | Download still exited 0; AzCopy may be better for future large artifact downloads |

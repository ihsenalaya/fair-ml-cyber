# Testing and Experiment Log - FAIR-ML-CYBER

This file records verification runs and experiment runs used for the article.

Rules:

- No invented metrics.
- Every reported metric must come from a real command output or a saved artifact.
- Every experiment must record data size, feature tier, split, model, seed, runtime and output path.
- Smoke tests are clearly labelled as smoke tests and must not be reported as final scientific results.
- Full experiments must be separated from smoke/debug runs.

## Environment

Initial local environment observed on 2026-06-16:

| Item | Value |
|---|---|
| OS context | WSL/Linux shell under `/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir` |
| Python | Python 3.10.12 |
| Virtual environment | `/home/ihsen/.venvs/fair-ml-cyber` |
| Git | `/usr/bin/git` |
| GitHub CLI | `/usr/bin/gh`, authenticated as `ihsenalaya` |
| Terraform | `/snap/bin/terraform` |
| Azure CLI | `/usr/bin/az` |
| Docker | `/usr/bin/docker` |
| LaTeX | `pdflatex` and `latexmk` not available locally |
| Dataset path | `/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs` |
| Dataset size | about 1.9 GB, 18 CSV files |
| Local CPU | AMD Ryzen 7 PRO 7840U, 8 cores / 16 threads under Microsoft WSL virtualization |
| Local memory at first test run | 7.1 GiB total, 3.7 GiB available, 2.0 GiB swap |

Python package versions observed on 2026-06-16T21:36:46+02:00:

| Package | Version |
|---|---|
| fair-ml-cyber | 0.1.0 |
| pandas | 2.3.3 |
| numpy | 2.2.6 |
| scikit-learn | 1.7.2 |
| matplotlib | 3.10.9 |
| pytest | 9.1.0 |
| pyyaml | 6.0.3 |
| joblib | 1.5.3 |
| pyarrow | 24.0.0 |
| mlflow | 3.13.0 |

## Dependency Setup Attempts

| Timestamp | Command | Result | Notes |
|---|---|---|---|
| 2026-06-16 | `python3 -m venv .venv` | Failed | `ensurepip` unavailable; `python3.10-venv` missing |
| 2026-06-16 | `sudo apt-get install python3.10-venv` | Failed | sudo requires interactive password |
| 2026-06-16 | `python3 -m pip install --user virtualenv && python3 -m virtualenv .venv` | Cancelled | Creating the venv under `/mnt/c` was too slow for iterative experiments |
| 2026-06-16 | `python3 -m virtualenv /home/ihsen/.venvs/fair-ml-cyber` | Completed | User-space Linux filesystem venv used for experiments |
| 2026-06-16 | `/home/ihsen/.venvs/fair-ml-cyber/bin/python -m pip install -e . --no-deps` plus dependency installs | Completed | Installed project and required packages including MLflow |

## Unit Test Runs

To be filled from real command outputs.

| Timestamp | Command | Duration | Result | Notes |
|---|---|---:|---|---|
| 2026-06-16T21:36:46+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 3.51 s wall clock | Passed: 9 tests | CPU 146%; max RSS 188,088 KB; exit status 0; validates hashing, feature tiers, metrics and split helpers |
| 2026-06-16T21:40:00+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 3.44 s wall clock | Passed: 10 tests | CPU 145%; max RSS 187,920 KB; exit status 0; adds validation that rare classes do not crash split construction and that the non-stratified fallback is recorded in split metadata |
| 2026-06-16T21:46:00+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 3.28 s wall clock | Passed: 10 tests | CPU 155%; max RSS 188,044 KB; exit status 0; regression check after changing MLflow tracking from file store to SQLite |
| 2026-06-16 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 3.72 s wall clock | Passed: 11 tests | CPU 141%; max RSS 186,692 KB; exit status 0; adds validation that all-missing numeric columns are excluded from feature tiers after the `protocol` warning observed in the smoke run |

## Dataset Audit Runs

To be filled from real command outputs.

| Timestamp | Command | Duration | Rows | Files | Data hash | Output |
|---|---|---:|---:|---:|---|---|
| 2026-06-16T21:41:00+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m fair_ml_cyber.cli audit --csv-dir /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs --output-dir data/audit` | 2:57.52 wall clock | 2,438,052 | 18 | `f51899df9bd60758` | `data/audit/audit_summary.json`, `data/audit/file_summary.csv`, `data/audit/label_distribution.csv`, `data/audit/columns.csv`; CPU 29%; max RSS 253,132 KB; exit status 0 |

## Smoke Experiment Runs

Smoke runs are for pipeline validation only.

| Timestamp | Command | Duration | Sample size | Models | Splits | Feature tiers | Result file |
|---|---|---:|---:|---|---|---|---|
| 2026-06-16T21:45:00+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m fair_ml_cyber.cli run-smoke --csv-dir /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs --work-dir data/smoke --sample-per-file 2000 --seed 42` | 4.40 s wall clock | Not loaded | None completed | None completed | None completed | Failed before training: MLflow 3.13 rejected `file://` tracking backend; max RSS 252,316 KB; exit status 1. Fixed by switching tracking to local SQLite plus local artifact directory. |
| 2026-06-16T21:43:45+02:00 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m fair_ml_cyber.cli run-smoke --csv-dir /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs --work-dir data/smoke --sample-per-file 2000 --seed 42` | 7:51.54 wall clock | 31,394 rows | `logistic_regression`, `random_forest`, `hist_gradient_boosting` | `random_stratified`, `temporal`, `day_holdout_2017-07-07`, `scenario_holdout_Web`, `endpoint_pair_holdout` | `no_identity`, `deployment_safe` | `data/smoke/results/smoke_results.csv`; 30 MLflow runs in `data/smoke/mlflow.db`; CPU 121%; max RSS 2,243,572 KB; exit status 0. Smoke-only validation. Warnings observed: sklearn imputer skipped all-missing `protocol` feature, indicating that nonnumeric protocol values were coerced to missing and should be removed or encoded before final experiments. |

## Azure Infrastructure Runs

| Timestamp | Command | Duration | Result | Resources | Notes |
|---|---|---:|---|---|---|
| 2026-06-16 | `terraform init` in `infra/terraform/azure` | Not timed | Success | Providers: `azurerm v4.77.0`, `random v3.9.0` | Local provider setup only |
| 2026-06-16 | `terraform validate` in `infra/terraform/azure` | Not timed | Success | Terraform configuration valid | First validation warned about deprecated Key Vault argument; code was corrected and validation re-run successfully |
| 2026-06-16 | `terraform apply -auto-approve -var="subscription_id=ec0e829d-64e1-43fd-b721-ecf5b5112773" -var="location=westeurope"` | Not measured with `/usr/bin/time` | Success: 7 added, 0 changed, 0 destroyed | Resource group `rg-fmlcyber-westeurope`; workspace `mlw-fair-ml-cyber`; storage `stfmlcybercg9ypy`; key vault `kv-fmlcyber-cg9ypy`; Log Analytics `law-fmlcyber-cg9ypy`; Application Insights `appi-fmlcyber-cg9ypy` | Duration was visible in Terraform streaming output only, not captured as a precise wall-clock metric; do not report an exact apply duration in the article |
| 2026-06-16 | `az ml workspace show --resource-group rg-fmlcyber-westeurope --name mlw-fair-ml-cyber --output json` | Not timed | Success | Azure ML workspace visible; MLflow URI `azureml://westeurope.api.azureml.ms/mlflow/v1.0/subscriptions/ec0e829d-64e1-43fd-b721-ecf5b5112773/resourceGroups/rg-fmlcyber-westeurope/providers/Microsoft.MachineLearningServices/workspaces/mlw-fair-ml-cyber` | Confirms visibility in Azure ML after Terraform apply |
| 2026-06-16 | `/usr/bin/time -v az ml compute create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --name cpu-cluster --type amlcompute --size Standard_DS3_v2 --min-instances 0 --max-instances 2 --idle-time-before-scale-down 120 --output json` | 2:13.43 wall clock | Success | Azure ML compute `cpu-cluster`, `Standard_DS3_v2`, min 0, max 2, provisioning state `Succeeded` | CPU 11%; max RSS 210,616 KB; exit status 0; no permanent VM node requested because `min_instances=0` |
| 2026-06-16 | `az resource show --ids /subscriptions/ec0e829d-64e1-43fd-b721-ecf5b5112773/resourceGroups/rg-fmlcyber-westeurope/providers/Microsoft.MachineLearningServices/workspaces/mlw-fair-ml-cyber --query ... --output table` | Not timed | Success | Workspace `mlw-fair-ml-cyber`, resource group `rg-fmlcyber-westeurope`, location `westeurope`, provisioning state `Succeeded` | Independent Azure Resource Manager verification after user reported not seeing Azure ML in the portal |
| 2026-06-16 | `az ml workspace list --resource-group rg-fmlcyber-westeurope --query ... --output table` | Not timed | Success | Azure ML workspace list contains `mlw-fair-ml-cyber` | Confirms the workspace exists from the Azure ML extension perspective |
| 2026-06-16 | `az ml compute list --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --query ... --output table` | Not timed | Success | Compute `cpu-cluster`, `Standard_DS3_v2`, min 0, max 2, provisioning state `Succeeded` | Confirms compute visibility in Azure ML |
| 2026-06-16 | `/usr/bin/time -v az ml environment create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file azureml/environment.yml --output json` | 1:01.27 wall clock | Success | Environment `fair-ml-cyber-env:1`, image `mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04`, conda file `azureml/conda.yml` | CPU 22%; max RSS 209,968 KB; exit status 0 |
| 2026-06-16 | `/usr/bin/time -v az ml data create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --name fair_ml_cyber_csvs --version 1 --type uri_folder --path /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs --output json` | Incomplete capture | No verified asset | Intended asset `fair_ml_cyber_csvs:1` | The command process continued after the user interrupted the turn and exited at 2026-06-16T22:19:27+02:00. Subsequent `az ml data show` returned 404 NotFound and `az ml data list` did not list the asset. The exact process output/exit status was not captured, so the cause must not be inferred. A second upload is being run with persistent logs. |

## Full Experiment Runs

Only these can be used as scientific results if completed and verified.

| Timestamp | Command | Duration | Rows | Models | Splits | Feature tiers | Result file |
|---|---|---:|---:|---|---|---|---|

## Resource Notes

For article-quality reporting, each experiment should record:

- CPU model or Azure VM SKU;
- number of cores;
- memory available;
- whether run was local or Azure ML;
- package versions;
- training runtime per model;
- inference runtime per 10,000 flows;
- artifact paths;
- MLflow run IDs.

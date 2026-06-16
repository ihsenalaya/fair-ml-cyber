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
| 2026-06-16 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 19.36 s wall clock | Failed: 1 of 12 tests | CPU 80%; max RSS 310,440 KB; exit status 1; first version of Azure ML/MLflow regression test incorrectly expected `MLFLOW_EXPERIMENT_ID` to remain absent after `mlflow.set_experiment()`, but MLflow repopulates it for the local experiment |
| 2026-06-16 | `/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q` | 13.80 s wall clock | Passed: 12 tests | CPU 91%; max RSS 310,552 KB; exit status 0; validates that `setup_mlflow()` clears Azure-injected `MLFLOW_RUN_ID` and does not retain the original Azure `MLFLOW_EXPERIMENT_ID` |

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
| 2026-06-16 | `/usr/bin/time -v az ml job create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file smoke_job.yml --output json` from `azureml/` | 2:18.55 wall clock | Pending | Pending | Pending | Pending | Azure ML job `sharp_leather_hdm3gxvqfx`, initial status `Starting`, Studio URL created; command submission CPU 16%, max RSS 221,240 KB, exit status 0. This is a smoke validation job. Azure ML recorded `azureml.git.dirty=True` because documentation/YAML changed after the first GitHub push; do not use this run as final article evidence without noting that flag. |
| 2026-06-16 | `az ml job create --file smoke_job.yml ... --skip-validation --set name=dryrun_should_not_submit` | Not timed | Not loaded | None completed | None completed | None completed | Accidental submission while checking CLI validation behavior. Job `dryrun_should_not_submit` failed immediately with the same Azure ML infrastructure issue as `sharp_leather_hdm3gxvqfx`; not used. |
| 2026-06-16 | `/usr/bin/time -v az ml job create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file smoke_job.yml --name smoke-runtime-001 --output json` from `azureml/` | 3:07.94 wall clock | Pending | Pending | Pending | Pending | Azure ML job `smoke-runtime-001`, initial status `Starting`, environment `fair-ml-cyber-runtime-env:1`, command installs dependencies at runtime; command submission CPU 16%, max RSS 220,028 KB, exit status 0. Azure ML still recorded `azureml.git.dirty=True`; do not use as final article evidence without noting that flag. |
| 2026-06-16 | Azure ML job `smoke-runtime-001` streamed with `az ml job stream` | Runtime 4:58 from StartTime to EndTime | Failed before model runs | None completed | None completed | None completed | Job ran from 2026-06-16 21:07:32 UTC to 21:12:30 UTC. The runtime environment and pip install succeeded, but user code failed at `mlflow.start_run()` because Azure ML injected `MLFLOW_RUN_ID=smoke-runtime-001` and the local SQLite MLflow store did not contain that run id. |
| 2026-06-16 | `/usr/bin/time -v az ml job create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file smoke_job.yml --name smoke-runtime-002 --output json` from `azureml/` | 2:57.01 wall clock | Pending | Pending | Pending | Pending | Azure ML job `smoke-runtime-002`, initial status `Starting`, environment `fair-ml-cyber-runtime-env:1`, `azureml.git.dirty=False`, git commit `a8bc4b75e61f7f21b51afd51e6fddd6ec55bc708`; command submission CPU 16%, max RSS 220,740 KB, exit status 0. |
| 2026-06-16 | Azure ML job `smoke-runtime-002` streamed, completed, downloaded, and summarized locally | Runtime 6:34 from 2026-06-16 21:21:07 UTC to 21:27:41 UTC | 31,394 rows sampled from 2,438,052 audited rows | `logistic_regression`, `random_forest`, `hist_gradient_boosting` | `random_stratified`, `temporal`, `day_holdout_2017-07-07`, `scenario_holdout_Web`, `endpoint_pair_holdout` | `no_identity`, `deployment_safe` | `data/azure_jobs/smoke-runtime-002/named-outputs/work_dir/results/smoke_results.csv`; `smoke_summary.json`; 30 runs; artifact summary command found 1 result file and 1 summary file; macro-F1 mean 0.585696, min 0.106431, max 0.997306; balanced accuracy mean 0.730648; AUROC mean 0.928488. Status `Completed`. Smoke-only validation; not final scientific evidence. |

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
| 2026-06-16 | `terraform plan -var="subscription_id=ec0e829d-64e1-43fd-b721-ecf5b5112773" -var="location=westeurope" -out=tfplan` after adding `container_registry_id` | Not applied | Rejected plan | Terraform proposed creating ACR `acrfmlcybercg9ypy` but also replacing Azure ML workspace `mlw-fair-ml-cyber` | Plan showed `azurerm_machine_learning_workspace.main must be replaced` because `container_registry_id` forces replacement. The plan was not applied and the Terraform change was reverted to avoid destroying/recreating the workspace and data assets. |
| 2026-06-16 | `/usr/bin/time -v az ml environment create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file azureml/environment_runtime.yml --output json` | 1:31.68 wall clock | Success | Environment `fair-ml-cyber-runtime-env:1`, image-only `mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04` | CPU 18%; max RSS 210,144 KB; exit status 0. This environment avoids Azure ML image build/ACR usage; dependencies are installed by the job command. |
| 2026-06-16 | `/usr/bin/time -v az ml data create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --name fair_ml_cyber_csvs --version 1 --type uri_folder --path /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs --output json` | Incomplete capture | No verified asset | Intended asset `fair_ml_cyber_csvs:1` | The command process continued after the user interrupted the turn and exited at 2026-06-16T22:19:27+02:00. Subsequent `az ml data show` returned 404 NotFound and `az ml data list` did not list the asset. The exact process output/exit status was not captured, so the cause must not be inferred. A second upload is being run with persistent logs. |
| 2026-06-16 | `/usr/bin/time -v az ml data create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file azureml/data_csvs.yml --output json` with local path | Aborted | Stopped intentionally | Azure ML CLI local upload attempt | Persistent log `logs/azure_data_create_v1.log` showed Azure ML warning that files exceed 100 MB and recommended AzCopy. Observed progress was too slow for a 1.95 GB dataset, so the process was terminated; the terminal reported exit code 143. This run is not a failed scientific experiment, only an infrastructure upload attempt. |
| 2026-06-16 | AzCopy install from Microsoft `aka.ms/downloadazcopy-v10-linux` | Not timed | Success | `/home/ihsen/.local/bin/azcopy`, version `10.32.4` | User-space install; no system package changes |
| 2026-06-16 | `/usr/bin/time -v /home/ihsen/.local/bin/azcopy copy <local CSV folder> <workspaceblobstore>/datasets/fair_ml_cyber_csvs/v1 --recursive=true --overwrite=true` | 4:57.30 wall clock | Success | 18 files transferred, 1,952,390,012 bytes, 0 failed, final job status `Completed` | CPU 116%; max RSS 2,002,816 KB; exit status 0. The raw AzCopy log files were deleted because they can contain temporary SAS material; the reproducible facts are recorded here. |
| 2026-06-16 | `az storage blob list --account-name stfmlcybercg9ypy --container-name azureml-blobstore-2250be0e-5ea0-44da-8ba7-01a76ed44d0c --prefix datasets/fair_ml_cyber_csvs/v1 --auth-mode key --query ... --output json` | Not timed | Success | 18 blobs, 1,952,390,012 bytes | `--auth-mode login` first failed because the signed-in user lacks a Storage Blob Data Reader/Contributor role on the storage account; verification succeeded through account-key auth |
| 2026-06-16 | `/usr/bin/time -v az ml data create --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --file azureml/data_csvs.yml --output json` with datastore path | 1:54.24 wall clock | Success | Azure ML data asset `fair_ml_cyber_csvs:1`, type `uri_folder`, path `azureml://.../datastores/workspaceblobstore/paths/datasets/fair_ml_cyber_csvs/v1/` | CPU 12%; max RSS 209,924 KB; exit status 0 |
| 2026-06-16 | `az ml data show --resource-group rg-fmlcyber-westeurope --workspace-name mlw-fair-ml-cyber --name fair_ml_cyber_csvs --version 1 --query ... --output json` | Not timed | Success | `fair_ml_cyber_csvs:1` visible in Azure ML | Confirms the final asset exists after datastore registration |

## Full Experiment Runs

Only these can be used as scientific results if completed and verified.

Current status on 2026-06-16: no full experiment has completed yet. The completed local and Azure ML runs above validate ingestion, audit, feature tiers, splitting, model training, metrics, MLflow logging and artifact download, but they remain smoke/debug evidence.

| Timestamp | Command | Duration | Rows | Models | Splits | Feature tiers | Result file |
|---|---|---:|---:|---|---|---|---|

## Bugs, Failures, and Operational Issues

This section records problems observed during implementation and experimentation. These issues must not be hidden in the article workflow. If a run is used in the paper, any relevant limitation below must be reflected in the method, threat-to-validity, reproducibility or appendix sections.

| Timestamp | Area | Symptom | Verified Cause | Action Taken | Status | Article Impact |
|---|---|---|---|---|---|---|
| 2026-06-16 | Local Python environment | `python3 -m venv .venv` failed | `ensurepip` / `python3.10-venv` unavailable in the system Python | Used user-space `virtualenv` and created `/home/ihsen/.venvs/fair-ml-cyber` outside `/mnt/c` | Resolved | Report local environment setup; do not assume system venv support |
| 2026-06-16 | Local Python environment | Attempted venv under `/mnt/c` was too slow | Windows-mounted filesystem caused poor iterative package setup performance | Moved venv to Linux filesystem under `/home/ihsen/.venvs` | Resolved | Local runtime measurements should mention WSL and filesystem context |
| 2026-06-16 | MLflow | Local smoke run failed before training | MLflow 3.13 rejects filesystem tracking backend by default unless explicitly allowed | Changed local tracking to SQLite `mlflow.db` plus local artifact directory | Resolved | Reproducibility section should specify MLflow backend |
| 2026-06-16 | Data splitting | Potential crash with rare labels during stratified splits | Some labels have extremely low support, e.g. `Heartbleed` has 12 rows and `Web_SQL_Injection` has 24 rows in the full dataset; split subsets can make strict stratification impossible | Added safe stratification fallback and metadata recording; added unit test for rare-class fallback | Resolved | Must report whether each split was stratified or fell back to non-stratified splitting |
| 2026-06-16 | Feature engineering | sklearn warned that `protocol` had no observed values in some training subsets | Local parser coerced nonnumeric `protocol` values to missing; all-missing numeric columns were still selected as features | Excluded all-missing numeric columns from feature tiers; added regression test | Resolved for future runs | The first local smoke run has this warning and is not final evidence |
| 2026-06-16 | Azure visibility | User could not see Azure ML in Azure Portal | CLI verification showed workspace existed in subscription `Abonnement Visual Studio Enterprise - MPN`, tenant `Répertoire par défaut`, resource group `rg-fmlcyber-westeurope` | Verified with `az resource show`, `az ml workspace show`, `az ml workspace list` and `az ml compute list` | Resolved from CLI; portal view may depend on selected directory/subscription filters | Article infrastructure appendix can cite verified resource IDs, not portal screenshots |
| 2026-06-16 | Azure ML data upload | First `az ml data create` process ended but asset did not exist | Exact process output was lost after user interruption; subsequent `az ml data show` returned 404 | Recorded as incomplete capture; reran with persistent logging | Resolved by later AzCopy workflow | Do not infer root cause for the first attempt |
| 2026-06-16 | Azure ML data upload | Second direct Azure ML CLI upload was too slow | Azure ML CLI warned that files exceed 100 MB and recommended AzCopy; observed progress was too slow for 1.95 GB | Stopped upload and installed AzCopy 10.32.4 in user space | Resolved | Dataset upload method should be documented as AzCopy to datastore plus asset registration |
| 2026-06-16 | Azure Storage verification | `az storage blob list --auth-mode login` failed | Signed-in user lacked Storage Blob Data Reader/Contributor role on the storage account | Verified blob upload using account-key auth; no RBAC role change applied | Workaround used | Infrastructure notes should mention RBAC limitation if reproducing with `auth-mode login` |
| 2026-06-16 | Git provenance | Early Azure ML job metadata recorded `azureml.git.dirty=True` | Files changed after the initial GitHub push before job submission | Committed and pushed the code fix before rerun; `smoke-runtime-002` recorded `azureml.git.dirty=False` at commit `a8bc4b75e61f7f21b51afd51e6fddd6ec55bc708` | Resolved for `smoke-runtime-002`; enforce again before final experiments | Runs with `dirty=True` must not be presented as clean final evidence |
| 2026-06-16 | Azure ML smoke job | Job `sharp_leather_hdm3gxvqfx` status is `Failed` | `az ml job stream` returned Azure ML execution error: `Disabling public network access is not supported for the SKU Basic`, referencing ACR private-link behavior; StartTime and EndTime were identical, so user code did not run | Did not use metrics; investigated ACR/Workspace remediation; used image-only runtime environment to bypass Azure ML image build/ACR path | Resolved diagnostically; smoke workload later completed as `smoke-runtime-002` | This run cannot be used as evidence; infrastructure failure only |
| 2026-06-16 | Azure ML smoke job | Attempted Terraform fix by adding Premium ACR to workspace | Terraform showed adding `container_registry_id` forces replacement of the existing Azure ML workspace | Reverted Terraform change and did not apply the plan | Resolved safely | Demonstrates why destructive infra changes must be reviewed before apply |
| 2026-06-16 | Azure ML operations | Job `dryrun_should_not_submit` was submitted accidentally while testing CLI options | `az ml job create --skip-validation` still submits a job; it is not a dry-run option | Attempted cancellation; job had already failed immediately | Closed | Must not be treated as experiment run |
| 2026-06-16 | Azure ML smoke job | Need to avoid Azure ML environment image build/ACR path | Conda-based environment can trigger image build path that failed with Basic ACR network setting | Created image-only runtime environment and changed job command to install dependencies at runtime | Workaround validated by `smoke-runtime-002` | Runtime dependency install adds startup overhead; record in resource/runtime reporting |
| 2026-06-16 | Azure ML smoke job | `smoke-runtime-001` failed after dependencies installed and package built | Azure ML injected `MLFLOW_RUN_ID=smoke-runtime-001`; local SQLite MLflow tracking then attempted to resume a run id that does not exist in the local store | Updated `setup_mlflow()` to clear `MLFLOW_RUN_ID` and stale Azure `MLFLOW_EXPERIMENT_ID`; added regression test | Resolved by local tests and successful Azure rerun `smoke-runtime-002` | No smoke metrics from `smoke-runtime-001`; useful only for diagnosing Azure ML environment/runtime behavior |
| 2026-06-16 | Local tests | First regression test for Azure ML MLflow environment failed | Test assumed `MLFLOW_EXPERIMENT_ID` would remain absent, but MLflow sets it after `set_experiment()` | Corrected assertion to ensure the original Azure experiment id is not retained | Resolved | Shows why test failures are preserved rather than hidden |
| 2026-06-16 | Azure ML smoke job | `smoke-runtime-002` completed successfully but uses a small sample | The job intentionally used `sample_per_file=2000` for pipeline validation, giving 31,394 sample rows rather than the full 2,438,052 rows | Downloaded and summarized artifacts; kept run in the smoke section only | Closed as validation run | Can support reproducibility/pipeline validation, but not final Q1-level empirical claims |
| 2026-06-16 | Azure ML artifact download | `az ml job download --all` emitted large-file/AzCopy-style warnings while still exiting successfully | Artifact bundle is large because it includes models, figures, MLflow database and logs | Verified downloaded files with `find`; read `smoke_summary.json` and `smoke_results.csv` locally | Closed | Artifact paths can be cited; warning is operational, not a failed experiment |
| 2026-06-16 | Azure CLI operations | `az ml job show` query for `smoke-runtime-002` produced no output for more than two minutes and was interrupted | Cause not diagnosed; could be CLI extension latency or transient Azure API behavior | Did not use this command as evidence; relied on streamed logs and downloaded artifacts already verified locally | Open observation | Do not cite this interrupted command as a source for job status or metrics |

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

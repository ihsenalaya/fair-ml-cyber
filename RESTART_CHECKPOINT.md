# Restart Checkpoint - 2026-06-17 11:47 Europe/Paris

This file records the exact state before the PC restart.

## Git state

- Last pushed commit before calibration work: `b6deadf Add Azure open-set baseline jobs`
- `b6deadf` was pushed to `main`.
- Azure jobs submitted from `b6deadf` have `azureml.git.dirty=False`.
- Local calibration runner files were added after `b6deadf` and should be committed/pushed before submitting calibration jobs.

## Local processes

Stopped local processes before restart:

- `az ml job stream ... --name advanced-core-s99-001`
- `/home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q`

Stopping the stream does not cancel the Azure ML job. Azure jobs continue on Azure.

## Azure jobs already submitted

Resource group: `rg-fmlcyber-westeurope`

Workspace: `mlw-fair-ml-cyber`

Compute: `cpu-memory-cluster` (`Standard_E8ds_v5`, max 1 node)

Submitted jobs:

| Job | Purpose | Last known state |
| --- | --- | --- |
| `advanced-core-s99-001` | Advanced full-data seed 99: binary, multiclass, rare-class, calibration bins, abstention, open-set uncertainty, explanation stability | `Running` via ARM status |
| `advanced-core-s7-001` | Advanced full-data seed 7 | `Queued` |
| `open-set-if-s42-001` | IsolationForest open-set baseline seed 42 | `Queued` |
| `open-set-if-s7-001` | IsolationForest open-set baseline seed 7 | `Queued` |
| `open-set-if-s99-001` | IsolationForest open-set baseline seed 99 | `Queued` |

Last streamed evidence for `advanced-core-s99-001`:

- `advanced_start` at `2026-06-17T09:32:18Z`
- LR binary `random_stratified` started at `2026-06-17T09:34:04Z`
- LR binary `random_stratified` completed at `2026-06-17T09:37:11Z`
- Result: `macro_f1=0.9338592853012393`, `ece=0.03407581212840107`, `convergence_warning_count=0`
- LR multiclass `random_stratified` started at `2026-06-17T09:37:11Z`

## Calibration work added locally

Added but not submitted at the moment this checkpoint was created:

- `src/fair_ml_cyber/calibration.py`
- CLI command: `run-calibration-baselines`
- Azure job files:
  - `azureml/calibration_seed42_job.yml`
  - `azureml/calibration_seed7_job.yml`
  - `azureml/calibration_seed99_job.yml`

Targeted validation completed:

```text
/usr/bin/time -v /home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest tests/test_advanced.py tests/test_modeling.py -q
4 passed, elapsed 0:38.54, max RSS 261684 KB, exit status 0
```

Full pytest was started after this but interrupted because the PC restart was requested. Do not record it as completed.

## Resume commands

Check job statuses:

```bash
cd /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/cyber
for job in advanced-core-s99-001 advanced-core-s7-001 open-set-if-s42-001 open-set-if-s7-001 open-set-if-s99-001; do
  echo "$job"
  az rest --method get \
    --url "https://management.azure.com/subscriptions/ec0e829d-64e1-43fd-b721-ecf5b5112773/resourceGroups/rg-fmlcyber-westeurope/providers/Microsoft.MachineLearningServices/workspaces/mlw-fair-ml-cyber/jobs/${job}?api-version=2024-04-01" \
    --query properties.status -o tsv
done
```

Stream the running job:

```bash
az ml job stream \
  --resource-group rg-fmlcyber-westeurope \
  --workspace-name mlw-fair-ml-cyber \
  --name advanced-core-s99-001
```

Download completed artifacts:

```bash
az ml job download \
  --resource-group rg-fmlcyber-westeurope \
  --workspace-name mlw-fair-ml-cyber \
  --name advanced-core-s99-001 \
  --download-path data/azure_jobs/advanced-core-s99-001 \
  --all
```

After download, copy the result CSVs into new `evidence/` folders following the existing pattern.

## Next work

1. Commit/push calibration runner if not already committed.
2. Submit calibration jobs:
   - `calibration-s42-001`
   - `calibration-s7-001`
   - `calibration-s99-001`
3. Wait for Azure jobs to finish.
4. Download artifacts into `data/azure_jobs/`.
5. Promote verified outputs to `evidence/`.
6. Update the article only with completed results.

## Resume Update - 2026-06-17 12:04 Europe/Paris

Completed after restart:

- Confirmed `main` is clean and aligned with `origin/main`.
- Confirmed calibration runner files are tracked and pushed in commit `be8cc11 Add calibration baseline checkpoint`.
- Submitted calibration jobs from clean git state (`azureml.git.dirty=False`, commit `be8cc111901d1ddc738f1c325282853ca5e8c50b`):
  - `calibration-s42-001`
  - `calibration-s7-001`
  - `calibration-s99-001`
- Completed local full pytest:

```text
/home/ihsen/.venvs/fair-ml-cyber/bin/python -m pytest -q
17 passed, 1 deprecation warning, exit status 0
```

Current Azure status via ARM after submissions:

| Job | Last checked state |
| --- | --- |
| `advanced-core-s99-001` | `Running` |
| `advanced-core-s7-001` | `Queued` |
| `open-set-if-s42-001` | `Queued` |
| `open-set-if-s7-001` | `Queued` |
| `open-set-if-s99-001` | `Queued` |
| `calibration-s42-001` | `Queued` |
| `calibration-s7-001` | `Queued` |
| `calibration-s99-001` | `Queued` |

Still pending:

1. Wait for Azure jobs to complete.
2. Download completed artifacts into `data/azure_jobs/`.
3. Promote verified text artifacts to `evidence/`.
4. Update `paper/main.tex` only with completed and locally verified results.

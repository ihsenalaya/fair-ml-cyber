# Ressources Azure pour FAIR-ML-CYBER

## Objectif

Utiliser Azure pour rendre les expériences de l'article reproductibles:

- stocker les CSV et outputs;
- lancer les pipelines ML;
- suivre les expériences avec MLflow;
- conserver les artefacts, modèles, métriques et figures;
- contrôler les coûts;
- pouvoir démontrer une traçabilité scientifique propre.

Le dataset local fait environ 1.9 Go et 2.44 millions de flux. Il ne nécessite pas une architecture Big Data lourde.

---

## Architecture minimale recommandée

### 1. Resource Group

Un groupe de ressources dédié:

`rg-fair-ml-cyber-dev`

Ressource réellement créée au 2026-06-16:

`rg-fmlcyber-westeurope`

Rôle:

- isoler toutes les ressources du projet;
- appliquer des tags;
- supprimer facilement l'environnement si besoin.

Tags recommandés:

- `project = fair-ml-cyber`
- `environment = dev`
- `owner = research`
- `cost_center = article`

---

### 2. Azure Storage Account

Ressource nécessaire.

Rôle:

- stocker les CSV bruts;
- stocker les datasets préparés;
- stocker les features;
- stocker les splits;
- stocker les figures;
- stocker les rapports et artefacts d'évaluation.

Containers proposés:

- `raw`: CSV originaux;
- `processed`: données nettoyées/parquet;
- `features`: feature tiers;
- `splits`: fichiers de split;
- `artifacts`: métriques, figures, rapports;
- `models`: modèles entraînés.

Pour ce projet, Blob Storage standard suffit. ADLS Gen2 peut être activé si on veut une structure plus data lake, mais ce n'est pas indispensable.

Ressource réellement créée:

`stfmlcybercg9ypy`

Le dataset brut a été uploadé dans le datastore Azure ML `workspaceblobstore` avec AzCopy, puis enregistré comme data asset:

`fair_ml_cyber_csvs:1`

Volume vérifié:

- 18 blobs;
- 1,952,390,012 bytes;
- 0 transfert échoué dans AzCopy.

---

### 3. Azure Machine Learning Workspace

Ressource centrale.

Rôle:

- lancer les jobs ML;
- gérer les data assets;
- gérer les environnements;
- centraliser les expériences;
- utiliser MLflow;
- conserver les logs et artefacts.

Azure ML Workspace est la ressource principale du projet. Microsoft décrit le workspace comme le point central pour suivre assets, ressources, logs et artefacts des workflows ML.

Workspace réellement créé:

`mlw-fair-ml-cyber`

Resource group:

`rg-fmlcyber-westeurope`

Région:

`westeurope`

---

### 4. MLflow Tracking via Azure ML

Nécessaire pour l'article si on veut une traçabilité forte.

À logger pour chaque run:

- data hash;
- feature hash;
- split hash;
- seed;
- modèle;
- hyperparamètres;
- métriques;
- temps d'entraînement;
- temps d'inférence;
- figures;
- matrice de confusion;
- calibration curves;
- Cyber Transferability Score.

Azure Machine Learning est compatible MLflow et peut agir comme serveur MLflow sans configuration supplémentaire lourde.

---

### 5. Azure ML Compute Cluster CPU

Ressource nécessaire pour lancer les expériences proprement dans Azure.

Pour ce dataset, un cluster CPU suffit. Pas besoin de GPU pour commencer.

Configuration recommandée après tests réels:

- `min_nodes = 0`
- `max_nodes = 1` ou `2` selon budget;
- VM CPU avec au moins 64 Go RAM pour le full-data core actuel;
- low-priority / spot si disponible pour réduire le coût;
- arrêt automatique grâce au `min_nodes = 0`.

Exemples de tailles à tester selon disponibilité régionale:

- `Standard_DS3_v2`: suffisant pour smoke/pilote, insuffisant pour le full-data core observé;
- `Standard_E8ds_v5`: validé pour le full-data core LogisticRegression/HistGradientBoosting;
- tailles supérieures de série E: à considérer pour Random Forest full-data, multi-seed, SHAP ou modèles plus lourds.

Utilisation:

- audit dataset;
- génération des features;
- entraînement Random Forest / XGBoost / LightGBM;
- calcul des métriques;
- SHAP/permutation importance;
- génération des figures.

Compute réellement créé:

`cpu-cluster`

Configuration:

- VM size: `Standard_DS3_v2`;
- min instances: 0;
- max instances: 2;
- idle scale-down: 120 s;
- provisioning state vérifié: `Succeeded`.

Cette taille a suffi pour:

- smoke Azure ML `smoke-runtime-002`: 31,394 lignes, 30 runs;
- pilote Azure ML `pilot10k-001`: 125,517 lignes, 30 runs.

Observation réelle au 2026-06-17:

- `fullcore-s42-001` sur `cpu-cluster` / `Standard_DS3_v2` a échoué par `SIGKILL`, probablement out-of-memory, dès le premier entraînement full-data;
- un cluster mémoire `cpu-memory-cluster` a été créé avec `Standard_E8ds_v5`, min 0, max 1, idle scale-down 120 s;
- le rerun `fullcore-mem-s42-001` via `azureml/full_core_memory_job.yml` a complété le full-data core: 2,438,052 lignes, 20/20 runs, 0 échec.
- la répétition `fullcore-mem-s7-001` via `azureml/full_core_memory_seed7_job.yml` a aussi complété 20/20 runs, 0 échec.

Conclusion opérationnelle:

- `Standard_DS3_v2` reste utile pour debug/smoke/pilote;
- `Standard_E8ds_v5` est la taille minimale validée pour le full-data core actuel sur deux seeds;
- les expériences finales plus lourdes doivent enregistrer coût, durée, mémoire, artefacts et éventuelles alertes de convergence.

---

### 6. Azure ML Compute Instance

Optionnel mais pratique.

Rôle:

- notebook de développement;
- exploration;
- debug;
- lancement manuel de jobs.

Si tu développes depuis ton PC local avec VS Code, ce n'est pas obligatoire. Pour économiser, on peut ne pas créer de compute instance et utiliser seulement des jobs sur compute cluster.

---

### 7. Key Vault

Recommandé.

Rôle:

- stocker secrets;
- stocker tokens éventuels;
- éviter de mettre des credentials dans le code.

Azure ML Workspace est généralement associé à Key Vault.

Key Vault réellement créé:

`kv-fmlcyber-cg9ypy`

---

### 8. Managed Identity et RBAC

Recommandé.

Rôle:

- permettre au workspace et aux jobs de lire/écrire dans le Storage Account;
- éviter les clés statiques;
- contrôler les droits.

Permissions typiques:

- `Storage Blob Data Contributor` pour l'identité du workspace ou du compute;
- accès Key Vault minimal si secrets nécessaires.

---

### 9. Azure Container Registry

Optionnel au début, recommandé pour reproductibilité forte.

Rôle:

- stocker les images Docker utilisées par les jobs;
- figer l'environnement Python;
- éviter les différences entre runs.

Si on utilise seulement des environnements Azure ML standards ou un conda environment simple, on peut différer ACR. Si l'article insiste sur reproductibilité, une image Docker versionnée est préférable.

Observation réelle:

- l'environnement Azure ML avec conda a déclenché un chemin de build image/ACR qui a échoué avec l'erreur `Disabling public network access is not supported for the SKU Basic`;
- une tentative Terraform d'ajouter un ACR Premium lié au workspace aurait forcé le remplacement du workspace Azure ML existant;
- cette modification destructive a été rejetée;
- contournement validé: environnement image-only `fair-ml-cyber-runtime-env:1` + installation pip au runtime.

Impact:

- le contournement fonctionne;
- il ajoute du temps de démarrage et des warnings pip root-user;
- pour un papier final, une image Docker versionnée ou un ACR propre devra être reconsidéré après sauvegarde des assets, sans remplacement destructif du workspace.

---

### 10. Application Insights / Log Analytics

Optionnel.

Rôle:

- logs d'exécution;
- monitoring;
- diagnostic.

Pour un article scientifique, les logs Azure ML + MLflow suffisent souvent. Application Insights/Log Analytics devient utile si on veut une observation plus cloud/ops.

Ressources réellement créées:

- Log Analytics workspace `law-fmlcyber-cg9ypy`;
- Application Insights `appi-fmlcyber-cg9ypy`.

---

### 11. Cost Management Budget

Nécessaire en pratique.

Rôle:

- éviter les coûts surprises;
- alerte email à 50%, 80%, 100% du budget;
- suivre les coûts par tags.

Les budgets Azure envoient des notifications quand les seuils sont dépassés, mais ils n'arrêtent pas automatiquement les ressources.

---

## Ressources non nécessaires

Pour cet article, ne pas créer au départ:

- Azure Databricks: trop lourd pour 1.9 Go;
- Synapse Analytics: inutile ici;
- AKS: pas besoin de déploiement production;
- Managed Online Endpoint: pas nécessaire pour écrire l'article;
- Event Hubs / Stream Analytics: pas de flux temps réel;
- Microsoft Sentinel: utile pour SOC réel, pas pour ce papier;
- GPU compute: pas nécessaire pour Random Forest, XGBoost, LightGBM, MLP simple.

---

## Pipeline Azure proposé

1. Upload CSV vers Storage: fait avec AzCopy.
2. Création data asset Azure ML `fair_ml_cyber_csvs:1`: fait.
3. Job Azure ML smoke `smoke-runtime-002`: fait, 30/30 runs complétés.
4. Job Azure ML pilote `pilot10k-001`: fait, 30/30 runs complétés.
5. Job Azure ML full-core `fullcore-s42-001` sur `Standard_DS3_v2`: échoué par SIGKILL/OOM, documenté.
6. Job Azure ML full-core mémoire `fullcore-mem-s42-001`: fait, 20/20 runs complétés sur `Standard_E8ds_v5`.
7. Job Azure ML full-core mémoire `fullcore-mem-s7-001`: fait, 20/20 runs complétés sur `Standard_E8ds_v5`.
8. `evaluate_transferability`: CTS macro-F1 initial multi-seed calculé dans `FULLCORE_MEM_MULTI_SEED_RESULTS.md`; version finale article à étendre.
9. `evaluate_calibration`: métriques Brier/ECE déjà sorties; reliability curves à ajouter.
10. `evaluate_explainability`: SHAP/permutation stability à ajouter.
11. `generate_figures`: partiel; figures article à produire après résultats finaux.
12. MLflow/logs: fonctionnel via SQLite local dans le work dir Azure, artefacts téléchargés.

---

## Configuration Azure minimale

| Besoin | Ressource Azure | Nécessité |
|---|---|---|
| Isolation projet | Resource Group | Obligatoire |
| Données et artefacts | Storage Account | Obligatoire |
| Tracking ML et orchestration | Azure ML Workspace | Obligatoire si Azure |
| Entraînement batch | Azure ML CPU Compute Cluster | Obligatoire si Azure |
| Secrets | Key Vault | Recommandé |
| Identité sécurisée | Managed Identity + RBAC | Recommandé |
| Docker reproductible | Container Registry | Optionnel puis recommandé |
| Exploration notebooks | Compute Instance | Optionnel |
| Monitoring avancé | App Insights / Log Analytics | Optionnel |
| Contrôle coûts | Cost Management Budget | Fortement recommandé |

---

## Recommandation finale

Etat actuel:

1. Resource Group: créé.
2. Storage Account: créé.
3. Azure ML Workspace: créé.
4. CPU Compute Cluster autoscale 0-2: créé.
5. Key Vault: créé.
6. Log Analytics / App Insights: créés.
7. Budget alert: à vérifier/configurer côté portail Azure si non existant.

Ajouter plus tard:

- Azure Container Registry ou image Docker versionnée, mais sans remplacement destructif du workspace existant;
- Compute Instance si le développement local devient pénible;
- rôle Storage Blob Data Contributor/Reader pour éviter le workaround account-key lors des vérifications blob.

## Runs Azure ML validés

| Job | Type | Données | Runs | Résultat | Notes |
|---|---|---:|---:|---|---|
| `smoke-runtime-002` | Smoke validation | 31,394 lignes | 30 | Completed | Valide pipeline Azure complet |
| `pilot10k-001` | Pilot experiment | 125,517 lignes | 30 | Completed | Signal scientifique fort mais non final |
| `fullcore-s42-001` | Full-data core attempt | 2,438,052 lignes chargées; first train split 1,706,636 lignes | 0 completed | Failed | `Standard_DS3_v2` OOM/SIGKILL before first model completed |

Job préparé pour la suite:

| Job YAML | Objectif | Artefacts |
|---|---|---|
| `azureml/full_core_job.yml` | Full-data core run avec Logistic Regression et HistGradientBoosting sur 5 splits et 2 tiers | `--no-save-models`, `--no-save-prepared` pour limiter le volume |
| `azureml/full_core_memory_job.yml` | Même protocole, mais sur `cpu-memory-cluster` / `Standard_E8ds_v5` après OOM DS3_v2 | `--no-save-models`, `--no-save-prepared` |

Artefacts locaux:

- `data/azure_jobs/smoke-runtime-002`;
- `data/azure_jobs/pilot10k-001`.

Ces dossiers sont ignorés par Git car ils contiennent des artefacts volumineux. Les faits reproductibles sont consignés dans `TESTING_AND_EXPERIMENT_LOG.md` et `PILOT10K_RESULTS.md`.

---

## Sources Microsoft consultées

- Azure ML workspace: https://learn.microsoft.com/en-us/cli/azure/ml/workspace
- Azure ML + MLflow: https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow
- Configuration MLflow Azure ML: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-configure-tracking
- Azure ML compute cluster: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster
- Azure ML compute instance: https://learn.microsoft.com/en-us/azure/machine-learning/concept-compute-instance
- Azure Cost Management budgets: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets
- Azure cost alerts: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending

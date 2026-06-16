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

Configuration recommandée:

- `min_nodes = 0`
- `max_nodes = 2` ou `4`
- VM CPU avec 16 a 32 Go RAM;
- low-priority / spot si disponible pour réduire le coût;
- arrêt automatique grâce au `min_nodes = 0`.

Exemples de tailles à tester selon disponibilité régionale:

- `Standard_D4ds_v5`: petit CPU, 16 Go RAM;
- `Standard_D8ds_v5`: plus confortable, 32 Go RAM;
- `Standard_E4ds_v5`: utile si mémoire plus importante.

Utilisation:

- audit dataset;
- génération des features;
- entraînement Random Forest / XGBoost / LightGBM;
- calcul des métriques;
- SHAP/permutation importance;
- génération des figures.

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

---

### 10. Application Insights / Log Analytics

Optionnel.

Rôle:

- logs d'exécution;
- monitoring;
- diagnostic.

Pour un article scientifique, les logs Azure ML + MLflow suffisent souvent. Application Insights/Log Analytics devient utile si on veut une observation plus cloud/ops.

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

1. Upload CSV vers Storage `raw/`.
2. Job Azure ML `audit_data`.
3. Job `prep_data`: nettoyage + conversion parquet.
4. Job `extract_features`: tiers de features.
5. Job `make_splits`: random, temporal, day, scenario, endpoint, open-set.
6. Job `train_model`: modèles ML.
7. Job `evaluate_model`: macro-F1, MCC, PR-AUC, AUROC.
8. Job `evaluate_transferability`: Cyber Transferability Score.
9. Job `evaluate_calibration`: Brier, ECE, reliability curves.
10. Job `evaluate_explainability`: SHAP/permutation stability.
11. Job `generate_figures`: figures article.
12. MLflow log toutes les métriques et artefacts.

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

Pour commencer sérieusement sans surcoût:

1. Resource Group.
2. Storage Account.
3. Azure ML Workspace.
4. CPU Compute Cluster autoscale 0-2.
5. Key Vault.
6. Managed Identity.
7. Budget alert.

Ajouter plus tard:

- Azure Container Registry pour Docker reproductible;
- Compute Instance si le développement local devient pénible;
- Log Analytics si besoin de monitoring avancé.

---

## Sources Microsoft consultées

- Azure ML workspace: https://learn.microsoft.com/en-us/cli/azure/ml/workspace
- Azure ML + MLflow: https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow
- Configuration MLflow Azure ML: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow-configure-tracking
- Azure ML compute cluster: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-create-attach-compute-cluster
- Azure ML compute instance: https://learn.microsoft.com/en-us/azure/machine-learning/concept-compute-instance
- Azure Cost Management budgets: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets
- Azure cost alerts: https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending

# ROADMAP - FAIR-ML-CYBER

## Sujet final

**FAIR-ML-CYBER: A Reproducible and Standardized Framework for Transferability Evaluation in Flow-Based Network Intrusion Detection**

Idée centrale:

> Adapter la logique de FAIR-ML-ICU à la cybersécurité: construire un framework reproductible, standardisé et tracké pour évaluer la portabilité des modèles ML de détection d'intrusion réseau entre jours, scénarios, services et attaques inconnues.

Dataset disponible:

`/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs`

Contrainte:

> un seul dataset disponible. On compense par des stress-tests intra-dataset rigoureux.

---

## Etat d'avancement vérifié au 2026-06-17

Travail terminé et vérifié:

- package Python `fair_ml_cyber` créé;
- dépôt GitHub privé créé et poussé: `https://github.com/ihsenalaya/fair-ml-cyber`;
- audit local complet des 18 CSV: 2,438,052 lignes, hash `f51899df9bd60758`;
- infrastructure Azure créée: resource group, storage, Key Vault, Log Analytics, Application Insights, Azure ML workspace, compute `cpu-cluster` et compute mémoire `cpu-memory-cluster`;
- data asset Azure ML `fair_ml_cyber_csvs:1` créé après upload AzCopy;
- smoke Azure ML `smoke-runtime-002` validé: 31,394 lignes, 30/30 runs complétés;
- moteur configurable `run-experiment` ajouté;
- pilote Azure ML `pilot10k-001` validé: 125,517 lignes, 30/30 runs complétés, 0 échec;
- artefacts pilote téléchargés et analysés localement;
- job full-data core `azureml/full_core_job.yml` préparé avec artefacts réduits puis soumis comme `fullcore-s42-001`;
- `fullcore-s42-001` a échoué par SIGKILL/OOM sur `Standard_DS3_v2` avant le premier modèle complet;
- cluster mémoire `cpu-memory-cluster` (`Standard_E8ds_v5`, min 0/max 1) créé;
- rerun mémoire `azureml/full_core_memory_job.yml` soumis comme `fullcore-mem-s42-001`;
- full-data core `fullcore-mem-s42-001` validé: 2,438,052 lignes, 20/20 runs complétés, 0 échec, artefacts téléchargés;
- synthèse full-data ajoutée dans `FULLCORE_MEM_S42_RESULTS.md`;
- bugs/dysfonctionnements documentés dans `TESTING_AND_EXPERIMENT_LOG.md`.

Signal scientifique observé dans le pilote et confirmé en full-data core:

- `random_stratified` donne des macro-F1 très élevées pour Random Forest et HistGradientBoosting;
- `temporal`, `day_holdout_2017-07-07` et `scenario_holdout_Web` révèlent des chutes importantes;
- Logistic Regression est moins spectaculaire en random split mais plus stable sur certains stress-tests temporels/day-holdout;
- en full-data core, HistGradientBoosting passe de 0.9978 macro-F1 en random split à 0.2316 en temporal et 0.3698 en day-holdout, tandis que LogisticRegression passe de 0.9364 à 0.5401 et 0.6388;
- le sujet "benchmark accuracy vs deployment reliability" est donc renforcé par des résultats réels full-data.

Ce qui n'est pas encore terminé:

- le full-data core binaire seed 42 est validé, mais pas encore répété multi-seed;
- Random Forest n'a pas encore été exécuté en full-data à cause du risque mémoire/artefacts;
- pas encore de répétitions multi-seed;
- CTS macro-F1 initial disponible dans `FULLCORE_MEM_S42_RESULTS.md`, mais CTS final multi-seed/multi-tâche à produire;
- pas encore d'analyse multi-classe/rare-class complète;
- pas encore de calibration/abstention complète;
- pas encore de LaTeX/PDF final.

---

## Contribution scientifique visée

Les modèles ML de détection d'intrusion réseau obtiennent souvent des scores très élevés sur des benchmarks comme CICIDS2017. Mais ces scores sont souvent produits avec des splits aléatoires, qui mélangent les mêmes jours, scénarios, services et endpoints entre train et test.

FAIR-ML-CYBER propose un framework reproductible pour mesurer non seulement la performance, mais surtout la **portabilité**:

- portabilité temporelle: train sur certains jours, test sur jours futurs;
- portabilité par scénario: train sur certaines campagnes d'attaque, test sur scénario non vu;
- portabilité par service: train sur certains ports/services, test sur autres;
- portabilité open-set: une famille d'attaque absente du train doit être détectée comme inconnue ou incertaine;
- portabilité des features: comparer features complètes vs features standardisées non fuitantes.

Score proposé:

**Cyber Transferability Score (CTS) = Metric_target / Metric_source**

Exemples:

- `CTS_F1 = macro_F1_target / macro_F1_source`
- `CTS_MCC = MCC_target / MCC_source`
- `CTS_PR_AUC = PR_AUC_target / PR_AUC_source`

Un score proche de 1 indique une meilleure portabilité.

---

## Phase 0 - Cadrage et audit des données

Durée estimée: 2-3 jours.

### Objectifs

- confirmer le schéma des CSV;
- documenter les labels;
- quantifier le déséquilibre;
- identifier les colonnes à risque de fuite;
- produire les premières tables pour l'article.

### Tâches

- [x] Charger les 18 CSV.
- [x] Créer une table unifiée avec `source_file`.
- [x] Ajouter `binary_label`: `Benign` vs `Attack`.
- [x] Ajouter `attack_family`: DoS, DDoS, Web, Botnet, PortScan, BruteForce, Heartbleed, Benign.
- [x] Parser `timestamp`.
- [x] Calculer:
  - nombre de flux par fichier;
  - nombre de flux par label;
  - distribution temporelle;
  - taux de classes rares;
  - schéma et colonnes requises;
  - hash dataset.
- [x] Identifier les colonnes potentiellement fuitantes:
  - `flow_id`;
  - `timestamp`;
  - `src_ip`;
  - `dst_ip`;
  - ports si fortement corrélés aux scénarios.
- [ ] Mesurer systématiquement doublons exacts et quasi-constantes pour le papier final.

### Livrables

- `data_audit_report.md`
- `label_distribution.csv`
- `feature_quality_report.csv`
- Figure: distribution des labels.
- Figure: timeline des scénarios.

---

## Phase 1 - Standardisation des features réseau

Durée estimée: 3-5 jours.

### Objectif

Créer une représentation standardisée, comparable et moins dépendante des artefacts de capture.

### Feature tiers

| Tier | Nom | Description |
|---|---|---|
| Tier 0 | Full-leaky | Toutes les colonnes, y compris identité/contexte |
| Tier 1 | No-identity | Sans `flow_id`, IPs, timestamp |
| Tier 2 | Flow-basic | Durée, protocole, paquets, bytes |
| Tier 3 | Flow-statistical | Stats payload, headers, IAT, flags TCP |
| Tier 4 | Deployment-safe | Features non identitaires et plausibles en SOC |

### Tâches

- [~] Définir les colonnes de chaque tier dans le code Python.
- [x] Créer un hash de chaque configuration de features.
- [x] Implémenter extraction/filtrage par tier.
- [x] Vérifier et exclure les colonnes numériques entièrement manquantes.
- [x] Normaliser les features pour les modèles qui le nécessitent via pipelines scikit-learn.
- [ ] Externaliser les tiers dans YAML si nécessaire pour l'article/reproductibilité.

### Livrables

- `config/features/full_leaky.yml`
- `config/features/no_identity.yml`
- `config/features/flow_basic.yml`
- `config/features/flow_statistical.yml`
- `config/features/deployment_safe.yml`
- Table: nombre de features par tier.

---

## Phase 2 - Pipeline reproductible FAIR-ML-CYBER

Durée estimée: 1 semaine.

### Objectif

Construire un pipeline exécutable de bout en bout:

CSV -> audit -> features -> splits -> training -> evaluation -> MLflow -> figures.

### Composants

1. `prep_data`: partiel via `load_csvs()` et `save_prepared()`.
2. `extract_features`: partiel via `select_feature_tier()`.
3. `make_splits`: partiel via `splits.py`.
4. `train_model`: fait pour les baselines actuelles via `modeling.py`.
5. `evaluate_model`: fait pour métriques binaires principales.
6. `evaluate_transferability`: à faire.
7. `evaluate_calibration`: partiel via Brier/ECE; figures à faire.
8. `evaluate_explainability`: à faire.
9. `generate_figures`: partiel via distribution labels et macro-F1 par split.

### Reproductibilité

Chaque run doit logger:

- git hash si disponible;
- data hash;
- feature hash;
- split hash;
- random seed;
- modèle;
- hyperparamètres;
- métriques;
- temps d'entraînement;
- temps d'inférence;
- MLflow run ID.

### Livrables

- `reproduce.sh`
- `requirements.txt`
- `README.md`
- `mlruns/` local ou tracking MLflow configurable.
- Script unique pour relancer toutes les expériences.

---

## Phase 3 - Protocoles de split et stress-tests

Durée estimée: 1 semaine.

### Objectif

Remplacer le split aléatoire unique par une suite de tests de portabilité.

### Splits

#### S0 - Random stratified split

Baseline classique.

- Train: 70%
- Validation: 15%
- Test: 15%

#### S1 - Temporal split

Train sur le passé, test sur le futur.

Exemple:

- Train: 2017-07-03 à 2017-07-05
- Validation: début 2017-07-06
- Test: fin 2017-07-06 et 2017-07-07

#### S2 - Day holdout

Tester la portabilité entre jours.

Exemples:

- train lundi-mardi-mercredi, test jeudi;
- train lundi-jeudi, test vendredi.

#### S3 - Scenario holdout

Tester une campagne absente du train.

Exemples:

- holdout Web attacks;
- holdout Botnet_ARES;
- holdout Port_Scan;
- holdout DDoS_LOIT.

#### S4 - Endpoint-pair holdout

Séparer les paires réseau:

`src_ip`, `dst_ip`, `dst_port`, `protocol`

Les mêmes paires ne doivent pas apparaître dans train et test.

#### S5 - Service/port holdout

Tester la robustesse par service:

- certains ports dans train;
- ports non vus dans test.

#### S6 - Open-set attack holdout

Retirer une famille d'attaque du train.

Le modèle doit classer:

- benign;
- known attack;
- unknown/review.

### Livrables

- `splits/random.yml`
- `splits/temporal.yml`
- `splits/day_holdout.yml`
- `splits/scenario_holdout.yml`
- `splits/endpoint_holdout.yml`
- `splits/open_set.yml`
- Table: résumé des splits.

---

## Phase 4 - Modèles ML

Durée estimée: 1 semaine.

### Modèles supervisés

- Logistic Regression;
- Random Forest;
- XGBoost ou LightGBM;
- MLP simple.

### Modèles open-set/anomaly

- Isolation Forest;
- One-Class SVM;
- Autoencoder simple;
- seuil d'incertitude sur probabilités;
- conformal prediction si possible.

### Tâches

- [ ] Implémenter config YAML par modèle.
- [x] Fixer seed dans les runs actuels.
- [x] Entraîner les baselines binaires sur splits principaux dans smoke/pilote.
- [~] Entraîner full-data/repeated-seed final: full-data core seed 42 validé pour LogisticRegression et HistGradientBoosting; répétitions multi-seed et Random Forest full-data restent à décider.
- [ ] Comparer classification binaire et multi-classe.
- [x] Mesurer temps d'entraînement et inférence dans les runs actuels.

### Livrables

- `config/models/logistic_regression.yml`
- `config/models/random_forest.yml`
- `config/models/xgboost.yml`
- `config/models/mlp.yml`
- `config/models/isolation_forest.yml`
- Table: hyperparamètres.

---

## Phase 5 - Métriques et portabilité

Durée estimée: 4-6 jours.

### Métriques classiques

- accuracy, secondaire seulement;
- macro-F1;
- weighted-F1;
- balanced accuracy;
- Matthews Correlation Coefficient;
- AUROC;
- PR-AUC;
- confusion matrix.

### Métriques classes rares

- recall par classe;
- precision par classe;
- F1 par classe;
- false negative rate par attaque;
- PR-AUC par classe.

### Métriques de portabilité

Définir:

`CTS(metric) = metric_stress_test / metric_random_split`

ou:

`CTS(metric) = metric_target / metric_source`

Exemples:

- CTS_macro_F1;
- CTS_MCC;
- CTS_PR_AUC.

### Métriques open-set

- known/unknown AUROC;
- unknown detection recall;
- false unknown rate;
- coverage/risk si abstention.

### Livrables

- Table principale: modèles x splits x metrics.
- Table portabilité: CTS par modèle et split.
- Figure: chute de performance entre random split et stress-tests.

---

## Phase 6 - Calibration, abstention et explicabilité

Durée estimée: 1 semaine.

### Calibration

Mesurer:

- Brier score;
- Expected Calibration Error;
- reliability diagram.

### Abstention

Approches:

- seuil sur probabilité max;
- seuil sur entropie;
- conformal prediction.

Métriques:

- coverage;
- selective risk;
- taux de cas envoyés à l'analyste;
- recall attaque après abstention.

### Explicabilité stable

Méthodes:

- permutation importance;
- SHAP si coût acceptable.

Mesurer:

- top-k feature overlap;
- corrélation de rang entre splits;
- stabilité par famille d'attaque;
- impact des features suspectes.

### Livrables

- Figure: reliability curves.
- Figure: coverage-risk curve.
- Figure: stabilité des top-k features.
- Table: features dominantes par split.

---

## Phase 7 - Analyse scientifique

Durée estimée: 1 semaine.

### Questions à répondre

1. Le split aléatoire surestime-t-il les performances?
2. Les features standardisées réduisent-elles la dépendance aux artefacts?
3. Quels modèles gardent le meilleur CTS?
4. Quelles classes rares restent mal détectées?
5. L'open-set detection est-elle possible avec ce dataset?
6. Les explications restent-elles stables?
7. Quel modèle est le meilleur compromis performance/coût?

### Résultats attendus

- performance élevée en random split;
- baisse en temporal/scenario/endpoint holdout;
- classes rares fragiles;
- meilleur CTS pour certains modèles simples ou régularisés;
- explications instables si features fuitantes incluses;
- calibration utile pour prioriser les alertes SOC.

---

## Phase 8 - Rédaction de l'article

Durée estimée: 2-3 semaines.

### Structure recommandée

1. Introduction
2. Related Work
3. Dataset and Audit
4. FAIR-ML-CYBER Framework
5. Experimental Protocol
6. Results
7. Discussion
8. Threats to Validity
9. Conclusion
10. Reproducibility Statement

### Figures

| Figure | Contenu |
|---|---|
| Figure 1 | Architecture FAIR-ML-CYBER |
| Figure 2 | Timeline des scénarios |
| Figure 3 | Distribution des labels |
| Figure 4 | Random split vs stress-tests |
| Figure 5 | Cyber Transferability Score |
| Figure 6 | Rare attack performance |
| Figure 7 | Calibration / abstention |
| Figure 8 | Explanation stability |

### Tables

| Table | Contenu |
|---|---|
| Table 1 | Dataset summary |
| Table 2 | Feature tiers |
| Table 3 | Split protocols |
| Table 4 | Main results |
| Table 5 | CTS results |
| Table 6 | Rare-class results |
| Table 7 | Runtime and inference cost |

---

## Phase 9 - Soumission

Durée estimée: 1-2 semaines.

### Cible principale

**Computers & Security**

Raison:

- scope sécurité + ML;
- accepte les contributions dataset/benchmark/evaluation;
- plus réaliste que IEEE TIFS/TDSC avec un seul dataset.

### Cible secondaire

**Expert Systems with Applications**

Raison:

- bon fit ML appliqué;
- possible si la partie XAI/calibration/abstention est forte.

### Préprint

- arXiv après stabilisation des résultats.

---

## Minimum viable article

Si on veut avancer vite:

1. Audit dataset: fait.
2. Feature tiers: partiel mais fonctionnel.
3. Random split vs temporal split vs scenario holdout: pilote fait et full-data core seed 42 validé pour LogisticRegression/HistGradientBoosting.
4. Endpoint-pair holdout: pilote fait et full-data core seed 42 validé.
5. Random Forest + Logistic Regression + HistGradientBoosting: pilote fait; full-data core validé pour LogisticRegression/HistGradientBoosting; Random Forest full-data à décider selon mémoire/coût.
6. Macro-F1, MCC, PR-AUC: fait dans pilote et full-data core; CTS macro-F1 initial disponible.
7. Calibration simple: métriques Brier/ECE présentes; figures à ajouter.
8. Figures principales: partiel.

---

## Version forte Q1

Pour maximiser les chances:

1. Ajouter endpoint-pair holdout.
2. Ajouter service/port holdout.
3. Ajouter abstention/conformal prediction.
4. Ajouter SHAP/permutation stability.
5. Ajouter runtime/inference cost.
6. Publier code + configs + seeds + splits.

---

## Checklist finale avant soumission

- [ ] Tous les résultats viennent de runs réels.
- [ ] Aucun score inventé.
- [ ] Scripts reproductibles.
- [ ] Seeds fixées.
- [ ] Data hash loggé.
- [ ] Feature hash loggé.
- [ ] Split hash loggé.
- [ ] MLflow run IDs sauvegardés.
- [ ] Figures générées par script.
- [ ] Limites du single-dataset clairement assumées.
- [ ] Pas de claim "zero-day réel" sans nuance.

---

## Conclusion

FAIR-ML-CYBER est la meilleure adaptation de FAIR-ML-ICU avec les données disponibles.

Le sujet devient:

> mesurer la portabilité et la fiabilité des modèles ML de détection d'intrusion à travers des stress-tests reproductibles construits à partir d'un seul dataset flow-based.

Ce positionnement est plus solide qu'un simple article de classification et donne une trajectoire réaliste vers un journal Q1, surtout **Computers & Security**.

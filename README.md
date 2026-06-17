# Cyber Article Proposal

Ce dossier contient une proposition d'article construite autour des CSV présents dans:

`/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs`

Verdict rapide: ces données ne conviennent pas à l'article FAIR-ML-ICU, mais elles sont pertinentes pour un article en cybersécurité sur la détection d'intrusion réseau par apprentissage automatique.

Les fichiers ressemblent fortement à une variante dérivée de CICIDS2017: mêmes dates de scénario, mêmes attaques, mêmes labels principaux et données de flux réseau.

## Proposition retenue

Titre provisoire:

**From Benchmark Accuracy to Deployment Reliability: A Single-Dataset Stress-Test Framework for Flow-Based Network Intrusion Detection**

Contrainte retenue: **on utilise uniquement les CSV locaux**.  

L'idée n'est pas de publier un énième modèle qui annonce 99% d'accuracy sur CICIDS2017. Pour viser un journal Q1 avec un seul dataset, la contribution doit être méthodologique et critique:

- montrer que les performances classiques sont probablement gonflées par des splits aléatoires et des artefacts de scénario;
- proposer un protocole d'évaluation plus réaliste: split temporel, holdout par scénario, holdout par paires d'hôtes, open-set attack detection;
- traiter sérieusement les classes rares comme Heartbleed et Web SQL Injection;
- ajouter calibration, abstention/conformal prediction et explicabilité stable;
- fournir un benchmark reproductible et orienté déploiement SOC.

## Fichiers

- `dataset_audit.md`: audit synthétique des CSV locaux.
- `state_of_the_art.md`: état de l'art et limites connues.
- `ETAT_ART_BIBLIOGRAPHIE.md`: état de l'art prioritaire et bibliographie annotée.
- `references.bib`: références BibTeX pour la rédaction.
- `article_proposal_q1.md`: proposition détaillée d'article.
- `experimental_protocol.md`: protocole expérimental concret.
- `bibliography.md`: sources consultées.
- `q1_viability_check.md`: verification critique de la faisabilite Q1.
- `single_dataset_q1_strategy.md`: solution finale avec un seul dataset.
- `ROADMAP_FAIR_ML_CYBER.md`: roadmap complète depuis les CSV jusqu'au papier.
- `RESEARCH_QUESTIONS_AND_PROTOCOL.md`: questions de recherche, hypothèses et protocole expérimental détaillé.
- `AZURE_RESOURCES.md`: ressources Azure nécessaires pour exécuter le travail de l'article.
- `TESTING_AND_EXPERIMENT_LOG.md`: journal vérifiable des tests, runs, durées, ressources, bugs et dysfonctionnements.
- `PILOT10K_RESULTS.md`: synthèse vérifiée du pilote Azure ML `pilot10k-001`.

## Etat actuel au 2026-06-16

Le projet n'est plus seulement au stade proposition. Un pipeline reproductible existe dans le package Python `fair_ml_cyber`:

- audit des 18 CSV;
- chargement et préparation des données;
- feature tiers `no_identity` et `deployment_safe`;
- splits `random_stratified`, `temporal`, `day_holdout`, `scenario_holdout_Web`, `endpoint_pair_holdout`;
- entraînement `logistic_regression`, `random_forest`, `hist_gradient_boosting`;
- métriques macro-F1, balanced accuracy, MCC, AUROC, AUPRC, Brier score, ECE;
- logging MLflow local SQLite;
- sorties CSV/JSON/JSONL, figures et modèles;
- exécution Azure ML via `azureml/smoke_job.yml` et `azureml/pilot_job.yml`.
- préparation du job full-data léger `azureml/full_core_job.yml`.

Ressources Azure créées et validées:

- resource group `rg-fmlcyber-westeurope`;
- workspace Azure ML `mlw-fair-ml-cyber`;
- storage `stfmlcybercg9ypy`;
- compute `cpu-cluster`, `Standard_DS3_v2`, min 0, max 2;
- data asset Azure ML `fair_ml_cyber_csvs:1`.

Runs vérifiés:

- audit local complet: 2,438,052 lignes, 18 fichiers, hash `f51899df9bd60758`;
- smoke Azure ML `smoke-runtime-002`: 31,394 lignes échantillonnées, 30/30 runs complétés;
- pilote Azure ML `pilot10k-001`: 125,517 lignes échantillonnées, 30/30 runs complétés, artefacts téléchargés localement.

Le pilote `pilot10k-001` montre déjà le signal scientifique central: les splits aléatoires donnent des scores quasi parfaits, alors que les splits temporels, day-holdout et scénario Web révèlent des chutes fortes de macro-F1. Ce résultat reste un **pilote**, pas encore la preuve finale de l'article.

Depuis le 2026-06-17, `azureml/full_core_job.yml` a été soumis comme `fullcore-s42-001` sur `Standard_DS3_v2`, mais il a échoué par `SIGKILL`, probablement out-of-memory, avant la fin du premier modèle full-data. Un cluster mémoire `cpu-memory-cluster` (`Standard_E8ds_v5`, min 0, max 1) a été créé, et le rerun versionné est `azureml/full_core_memory_job.yml`.

## Positionnement Q1

Cible la plus cohérente: **Computers & Security**.

Cibles plus ambitieuses ou alternatives:

- **IEEE Transactions on Dependable and Secure Computing**
- **IEEE Transactions on Information Forensics and Security**
- **Expert Systems with Applications**

Important: un papier basé uniquement sur un modèle ML classique et CICIDS2017 sera probablement trop faible pour du Q1. La valeur doit venir de la rigueur expérimentale, de l'analyse des biais du benchmark et du protocole réutilisable.

## Prochaine étape

La prochaine étape scientifique est de transformer le pilote en protocole final:

- décider quelles expériences doivent être full-data et lesquelles doivent être répétées par seed;
- éviter de sauvegarder tous les modèles si les artefacts deviennent trop lourds;
- ajouter les métriques de portabilité CTS;
- ajouter les analyses rare-class, calibration, abstention et éventuellement explainability;
- produire ensuite l'article LaTeX/PDF uniquement à partir des résultats vérifiés.

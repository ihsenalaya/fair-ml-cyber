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

## Positionnement Q1

Cible la plus cohérente: **Computers & Security**.

Cibles plus ambitieuses ou alternatives:

- **IEEE Transactions on Dependable and Secure Computing**
- **IEEE Transactions on Information Forensics and Security**
- **Expert Systems with Applications**

Important: un papier basé uniquement sur un modèle ML classique et CICIDS2017 sera probablement trop faible pour du Q1. La valeur doit venir de la rigueur expérimentale, de l'analyse des biais du benchmark et du protocole réutilisable.

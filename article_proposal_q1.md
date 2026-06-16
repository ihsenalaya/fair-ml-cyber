# Proposition d'Article Q1

## Titre provisoire final

**From Benchmark Accuracy to Deployment Reliability: A Single-Dataset Stress-Test Framework for Flow-Based Network Intrusion Detection**

Ancien titre possible:

**Beyond Near-Perfect Accuracy: A Leakage-Aware, Temporal, Open-Set and Explainable Evaluation Framework for Flow-Based Network Intrusion Detection**

## Message central

Les modèles de détection d'intrusion réseau rapportent souvent des performances quasi parfaites sur CICIDS2017. Mais ces résultats sont souvent obtenus avec des splits aléatoires et sans analyse systématique des fuites, de la temporalité, des classes rares et de l'explicabilité. Nous proposons un cadre d'évaluation plus proche d'un déploiement SOC, utilisant exclusivement les flux CICIDS2017-like disponibles localement.

## Angle Q1

L'article doit être **data-centric et evaluation-centric**, pas "model-centric".

Le point fort n'est pas de battre un score, mais de répondre à une question plus importante:

> Quels scores restent valides lorsque l'on retire les fuites de contexte et que l'on teste les modèles dans des conditions temporelles, open-set et opérationnelles?

Contrainte assumee dans le papier:

> L'etude utilise un seul dataset. Elle ne revendique pas une validation externe universelle; elle propose un protocole de stress-test intra-dataset reutilisable.

## Contributions proposées

### Contribution 1 - Audit reproductible des données

Produire un audit systématique des CSV:

- distribution des labels;
- déséquilibre extrême;
- features constantes ou quasi constantes;
- doublons exacts et quasi-doublons;
- timestamps par scénario;
- dépendance aux IPs, ports, protocoles et `flow_id`;
- détection des colonnes potentiellement fuitantes.

Livrable scientifique:

> une taxonomie des risques de fuite dans les datasets flow-based de type CICIDS2017.

### Contribution 2 - Benchmark anti-fuite

Comparer plusieurs protocoles de validation:

1. **Random stratified split**: baseline classique, probablement optimiste.
2. **Temporal split**: entraînement sur le passé, test sur le futur.
3. **Scenario holdout**: un ou plusieurs fichiers/scénarios entièrement réservés au test.
4. **Endpoint-pair holdout**: séparation par tuple réseau pour éviter que le modèle mémorise des communications.
5. **Open-set attack holdout**: une famille d'attaque est absente du train et doit être détectée comme inconnue/anormale.

Livrable scientifique:

> quantifier l'écart entre performance de laboratoire et performance déployable.

### Contribution 3 - Détection des classes rares

Heartbleed et Web SQL Injection sont extrêmement minoritaires. L'article doit montrer que l'accuracy globale est trompeuse.

Approches:

- métriques macro: macro-F1, balanced accuracy, MCC;
- PR-AUC par classe;
- recall par classe rare;
- hierarchical classification: benign/attack puis famille;
- focal loss ou class weights;
- comparaison avec anomaly detection pour classes rares.

Livrable scientifique:

> un protocole robuste pour évaluer les attaques rares sans masquer l'échec derrière une accuracy globale élevée.

### Contribution 4 - Calibration et abstention

Pour un SOC, une alerte non fiable coûte cher. L'article peut ajouter:

- Brier score;
- Expected Calibration Error;
- reliability diagrams;
- conformal prediction ou seuil d'abstention;
- métriques coverage/risk;
- taux d'alertes envoyées à analyste humain.

Livrable scientifique:

> un NIDS qui sait dire "attaque connue", "bénin" ou "incertain / review analyst".

### Contribution 5 - Explicabilité stable

Ne pas se contenter d'un graphique SHAP.

Mesurer:

- stabilité des top-k features entre splits;
- stabilité par famille d'attaque;
- différence d'explication entre random split et temporal split;
- influence des features potentiellement fuitantes;
- plausibilité opérationnelle des features dominantes.

Livrable scientifique:

> une méthode pour tester si les explications d'un NIDS sont robustes ou simplement liées aux artefacts du benchmark.

### Contribution 6 - Coût et déploiement

Comparer des familles de modèles:

- Logistic Regression;
- Random Forest;
- XGBoost/LightGBM;
- MLP simple;
- Autoencoder/anomaly detector pour open-set.

Mesurer:

- temps d'entraînement;
- temps d'inférence par 10 000 flux;
- mémoire;
- performance avec feature tiers réduits.

Livrable scientifique:

> un compromis performance/latence/explicabilité utile pour un déploiement SOC.

## Question de recherche principale

**RQ1.** Les performances quasi parfaites sur CICIDS2017 persistent-elles lorsque l'évaluation est temporelle, anti-fuite et open-set?

## Questions secondaires

**RQ2.** Quelles features expliquent réellement la détection, et ces explications restent-elles stables sous différents protocoles?

**RQ3.** Les attaques rares peuvent-elles être détectées avec des métriques fiables, ou les scores globaux les masquent-ils?

**RQ4.** La calibration et l'abstention réduisent-elles les fausses alertes sans dégrader excessivement la détection?

**RQ5.** Quel compromis modèle/features est réaliste pour une utilisation en SOC?

## Hypothèses

- **H1**: le split aléatoire surestime significativement les performances.
- **H2**: retirer les features d'identité ou de scénario réduit les scores mais améliore la crédibilité du modèle.
- **H3**: les classes rares sont mal représentées par l'accuracy globale.
- **H4**: l'abstention améliore le risque opérationnel en transférant les cas incertains à l'analyste.
- **H5**: les explications SHAP sont instables si le protocole laisse passer des artefacts de dataset.

## Structure de l'article

1. **Introduction**
   - NIDS flow-based et popularité des benchmarks.
   - Limite des scores quasi parfaits.
   - Besoin d'évaluation orientée déploiement.

2. **Related Work**
   - CICIDS2017 et datasets IDS.
   - Limites et erreurs de CICIDS2017.
   - Generalisation inter-datasets.
   - Feature standardization et NetFlow.
   - XAI, calibration, open-set detection.

3. **Dataset and Audit**
   - Description des 2.44M flux.
   - Labels et déséquilibre.
   - Risques de fuite.

4. **Methods**
   - Prétraitement.
   - Feature tiers.
   - Modèles.
   - Protocoles de split.
   - Calibration/abstention.
   - XAI stability.

5. **Results**
   - Random vs temporal vs scenario holdout.
   - Performance par classe.
   - Open-set detection.
   - Calibration.
   - Explicabilité.
   - Coût.

6. **Discussion**
   - Pourquoi les scores classiques sont trop optimistes.
   - Ce qui est réellement déployable.
   - Limites du dataset.

7. **Conclusion**
   - Benchmark reproductible et recommandations.

## Résumé provisoire

Machine-learning-based Network Intrusion Detection Systems often report near-perfect performance on benchmark datasets such as CICIDS2017. However, such results are frequently obtained under random splits and insufficient controls for temporal leakage, scenario memorization, rare attacks and calibration. This paper introduces a leakage-aware and deployment-oriented evaluation framework for flow-based NIDS. Using 2.44 million CICIDS2017-like network flows, we compare random, temporal, scenario, endpoint-pair and open-set evaluation protocols across classical and gradient-boosted models. We further assess rare-attack detection, probability calibration, abstention and explanation stability. The proposed framework quantifies the gap between laboratory performance and operational robustness, showing how evaluation choices affect reported detection capability and analyst-facing trust. The study provides a reproducible protocol and practical recommendations for robust NIDS benchmarking.

## Cibles de soumission

1. **Computers & Security** - cible principale, très adaptée au sujet dataset/NIDS/evaluation.
2. **Expert Systems with Applications** - si l'article met plus l'accent sur ML/XAI/calibration.
3. **IEEE Transactions on Dependable and Secure Computing** - plus ambitieux, demanderait une contribution plus forte côté sécurité/déploiement.
4. **IEEE Transactions on Information Forensics and Security** - possible mais probablement plus exigeant sur la nouveauté algorithmique.

## Risque principal

Un reviewer peut dire: "CICIDS2017 est trop ancien et trop étudié."

Réponse:

- ne pas revendiquer un nouveau SOTA sur CICIDS2017;
- revendiquer un cadre de validation critique;
- intégrer les limites connues;
- ajouter si possible un dataset externe plus tard: CSE-CIC-IDS2018, UNSW-NB15, ToN-IoT ou NF-UQ-NIDS-v2.

## Decision

La proposition est pertinente pour Q1 si elle est écrite comme un article de **méthodologie d'évaluation fiable**, pas comme un article de classification standard.

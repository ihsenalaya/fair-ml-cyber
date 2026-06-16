# Etat de l'Art

## 1. Dataset CICIDS2017 et contexte

Les CSV locaux correspondent très probablement à une version dérivée de **CICIDS2017**, un dataset créé par le Canadian Institute for Cybersecurity pour évaluer des systèmes de détection d'intrusion réseau. La page officielle indique que CICIDS2017 contient du trafic bénin et des attaques courantes, avec des flux labellisés à partir de timestamps, IPs, ports, protocoles et type d'attaque.

La contribution initiale de Sharafaldin, Lashkari et Ghorbani était de proposer un dataset plus réaliste que les anciens benchmarks IDS, avec des scénarios incluant DoS, DDoS, brute force, web attacks, botnet, infiltration et port scan.

## 2. Travaux classiques sur CICIDS2017

Une grande partie de la littérature utilise CICIDS2017 pour comparer des modèles supervisés:

- Random Forest, Decision Trees, SVM, k-NN, Naive Bayes;
- XGBoost, LightGBM, CatBoost;
- MLP, CNN, LSTM, autoencoders, transformers;
- feature selection, PCA, SMOTE/ADASYN, stacking/ensemble;
- XAI via SHAP/LIME.

Le problème: beaucoup de papiers rapportent des accuracy très élevées, parfois proches de 99%, mais avec des splits aléatoires et peu de contrôle de fuite. Pour du Q1, cette ligne est saturée.

## 3. Limites méthodologiques connues

### 3.1 Qualité et erreurs de dataset

Engelen, Rimmer et Joosen ont revisité CICIDS2017 et ont documenté des problèmes dans la génération du trafic, la construction des flux, l'extraction de features et le labelling. Leur analyse signale qu'une fraction importante des traces originales doit être reconstruite ou relabellisée pour améliorer la validité du benchmark.

Conséquence pour notre article: il faut intégrer une section explicite de **data audit** et ne pas supposer que les labels sont parfaits.

### 3.2 Generalisation faible

Des études récentes de généralisation inter-datasets montrent que les modèles NIDS peuvent obtenir des performances quasi parfaites lorsqu'ils sont entraînés et testés sur le même dataset, puis s'effondrer lorsqu'ils sont évalués sur un autre réseau ou un autre dataset. Cela renforce l'idée qu'une validation par split aléatoire n'est pas suffisante.

Conséquence pour notre article: le protocole doit mesurer la robustesse sous:

- split temporel;
- holdout par scénario;
- holdout par endpoints;
- open-set family holdout.

### 3.3 Absence de benchmark standardisé

Les surveys récents soulignent que les datasets NIDS publics sont nombreux mais hétérogènes, souvent peu comparables, et que les choix de preprocessing/split/métriques rendent les résultats difficiles à interpréter.

Conséquence pour notre article: proposer un **benchmark reproductible et transparent** est plus pertinent qu'un nouveau modèle isolé.

### 3.4 Problème des features non standardisées

Sarhan, Layeghy et Portmann ont montré que l'absence de feature set commun limite la comparaison et la généralisation des NIDS. Ils proposent des features NetFlow standardisées.

Conséquence pour notre article: exploiter les 122 features locales, mais comparer plusieurs niveaux de features:

- Tier A: features opérationnelles minimales sans IP, timestamp ni identifiant;
- Tier B: features de flux proches NetFlow;
- Tier C: toutes les statistiques flow-based disponibles;
- Tier D: features potentiellement fuitantes, pour démontrer l'écart.

### 3.5 Explicabilité insuffisante

La littérature XAI pour IDS utilise souvent SHAP/LIME pour expliquer un modèle, mais rarement pour vérifier si les explications sont stables entre splits ou plausibles opérationnellement.

Conséquence pour notre article: au lieu de simplement afficher des SHAP plots, mesurer:

- stabilité des top-k features;
- différence entre explications sous split aléatoire et split temporel;
- dépendance aux features d'identité comme IP/port/timestamp;
- cohérence par famille d'attaque.

## 4. Gap scientifique exploitable

Le gap le plus solide:

> Les travaux sur CICIDS2017 optimisent surtout l'accuracy dans des conditions de laboratoire. Peu d'études évaluent simultanément fuite expérimentale, généralisation temporelle, open-set attacks, classes rares, calibration, abstention et explicabilité stable.

## 5. Positionnement recommandé

Ne pas écrire:

> "Nous proposons un modèle deep learning qui atteint 99.8% d'accuracy sur CICIDS2017."

Ecrire plutôt:

> "Nous proposons un cadre d'évaluation reproductible pour distinguer performance de laboratoire et performance déployable des NIDS flow-based, en quantifiant l'impact des splits, des features potentiellement fuitantes, des attaques rares, de l'open-set detection, de la calibration et de l'explicabilité."

## 6. Sources principales

- Canadian Institute for Cybersecurity, CICIDS2017 official dataset page.
- Sharafaldin, Lashkari, Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", ICISSP 2018.
- Engelen, Rimmer, Joosen, "Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study", IEEE SPW 2021.
- Goldschmidt, Chuda, "Network intrusion datasets: A survey, limitations, and recommendations", Computers & Security, 2025.
- Cantone, Marrocco, Bria, "Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study", IEEE Access, 2024.
- Sarhan, Layeghy, Portmann, "Towards a Standard Feature Set for Network Intrusion Detection System Datasets", Mobile Networks and Applications, 2021.
- Sommer, Paxson, "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection", IEEE Symposium on Security and Privacy, 2010.

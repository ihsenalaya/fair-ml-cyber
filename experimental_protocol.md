# Protocole Experimental

## Objectif

Construire un benchmark reproductible permettant de mesurer ce qui reste des performances NIDS lorsque l'on impose des contraintes réalistes:

- pas de fuite par split aléatoire;
- généralisation temporelle;
- scénarios non vus;
- endpoints non vus;
- attaques inconnues;
- classes rares;
- calibration et abstention;
- coût d'inférence.

## Données d'entrée

CSV locaux:

`/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs/*.csv`

Unifier les fichiers dans une table commune:

- `source_file`;
- toutes les features originales;
- `label`;
- `binary_label`: `Benign` vs `Attack`;
- `attack_family`: DoS, DDoS, Web, Botnet, PortScan, BruteForce, Heartbleed, Benign.

## Preprocessing

### Colonnes à exclure par défaut

Exclure du modèle principal:

- `flow_id`;
- `timestamp`;
- `src_ip`;
- `dst_ip`.

Raison: ces colonnes risquent d'encoder le scénario de capture plutôt que le comportement réseau généralisable.

### Colonnes à tester séparément

Créer des variantes:

- avec ports;
- sans ports;
- avec protocol;
- sans protocol;
- features full;
- features compactes.

### Nettoyage

- convertir timestamps en datetime pour split uniquement;
- remplacer inf/nan;
- standardiser les colonnes numériques pour les modèles linéaires/MLP;
- conserver les valeurs brutes pour Random Forest/XGBoost/LightGBM;
- dédupliquer les lignes exactes avant split ou au minimum mesurer l'impact des doublons.

## Feature tiers

| Tier | Description | Colonnes |
|---|---|---|
| Tier 0 | Identité/scénario | IPs, timestamp, flow_id, exact ports |
| Tier 1 | Flux minimal | duration, protocol, packet counts, byte counts |
| Tier 2 | Flux statistique | payload stats, IAT stats, flags TCP |
| Tier 3 | Full non-identitaire | toutes les features sauf IP/timestamp/flow_id |
| Tier 4 | Full avec risque de fuite | toutes les features, uniquement pour démonstration |

Le papier doit présenter Tier 4 comme un contrôle, pas comme modèle recommandé.

## Protocoles de split

### P0 - Random stratified split

Baseline classique:

- train 70%;
- validation 15%;
- test 15%;
- stratification par label.

Utilité: montrer le score optimiste.

### P1 - Temporal split global

Trier par `timestamp`:

- train: premiers 60%;
- validation: 20% suivants;
- test: derniers 20%.

Utilité: éviter fuite temporelle.

Limite: certaines attaques sont concentrées sur un jour précis; il faut interpréter les absences de classes.

### P2 - Chronological split per class

Pour chaque classe, trier par timestamp puis séparer 70/15/15.

Utilité: tester l'autocorrélation intra-classe tout en gardant toutes les classes.

### P3 - Scenario/file holdout

Réserver des fichiers entiers au test:

- test DoS: `dos_*`;
- test Web: `web_*`;
- test Friday attacks: `portscan`, `botnet_ares`, `ddos_loit`;
- test rare attacks: `heartbleed`, `web_sql_injection`.

Utilité: éviter que les mêmes scénarios apparaissent dans train/test.

### P4 - Endpoint-pair holdout

Créer un groupe:

`endpoint_pair = src_ip + dst_ip + dst_port + protocol`

Séparer les groupes entre train et test.

Utilité: empêcher la mémorisation des communications.

### P5 - Open-set attack family holdout

Train:

- Benign;
- toutes les attaques sauf une famille.

Test:

- Benign;
- attaques connues;
- famille inconnue holdout.

Familles holdout recommandées:

- Web attacks;
- Botnet_ARES;
- Port_Scan;
- DDoS_LOIT;
- Heartbleed, avec prudence car seulement 12 lignes.

Sortie attendue:

- connu vs inconnu;
- score d'anomalie;
- abstention.

## Modèles

### Baselines

- Logistic Regression;
- Decision Tree;
- Random Forest;
- XGBoost ou LightGBM;
- MLP simple.

### Open-set/anomaly

- Isolation Forest;
- One-Class SVM sur benign;
- Autoencoder sur benign;
- softmax entropy / max probability threshold;
- conformal prediction.

## Métriques

### Classification globale

- Accuracy, uniquement comme métrique secondaire;
- balanced accuracy;
- macro-F1;
- weighted-F1;
- Matthews Correlation Coefficient;
- macro PR-AUC;
- AUROC binaire.

### Par classe

- precision;
- recall;
- F1;
- false positive rate;
- false negative rate;
- PR-AUC par classe.

### Classes rares

Rapporter séparément:

- Heartbleed;
- Web_SQL_Injection;
- Web_XSS;
- Web_Brute_Force.

Ne jamais conclure à une bonne performance rare-class depuis l'accuracy globale.

### Calibration

- Brier score;
- Expected Calibration Error;
- reliability diagrams;
- negative log likelihood.

### Abstention

- coverage;
- selective risk;
- taux de cas envoyés à l'analyste;
- recall sur attaques quand coverage varie.

### Temps et coût

- training time;
- inference time par 10 000 flux;
- mémoire du modèle;
- nombre de features.

## Analyses clés à produire

1. Tableau random vs temporal vs scenario holdout.
2. Matrice de confusion multi-classe pour P0 et P3.
3. Performance par classe rare.
4. Courbes PR pour classes rares.
5. Calibration curves.
6. Coverage-risk curve pour abstention.
7. SHAP top-k features et stabilité.
8. Impact des feature tiers.
9. Runtime/latency table.

## Figures publication-ready

- Figure 1: overview du framework expérimental.
- Figure 2: distribution temporelle des labels.
- Figure 3: chute de performance P0 -> P1/P3/P4/P5.
- Figure 4: rare-class PR curves.
- Figure 5: calibration and abstention.
- Figure 6: SHAP stability heatmap.
- Figure 7: performance vs inference cost.

## Validité et limites

Menaces à la validité:

- dataset de laboratoire, pas production;
- labels possiblement imparfaits;
- absence des PCAP originaux;
- timestamps concentrés par scénario;
- très peu d'échantillons pour certaines classes.

Mesures de mitigation:

- audit explicite;
- plusieurs protocoles;
- métriques macro et par classe;
- ne pas surinterpréter Heartbleed/SQL Injection;
- publier code, seeds, hashes et configs.

## Minimum viable paper

Pour un premier papier solide:

1. audit dataset;
2. P0/P1/P3/P5;
3. Random Forest + XGBoost + Logistic Regression + Isolation Forest;
4. macro-F1, MCC, PR-AUC par classe, calibration;
5. SHAP stability;
6. runtime.

Pour viser Q1 plus confortablement:

1. ajouter P4 endpoint holdout;
2. ajouter conformal prediction/abstention;
3. ajouter un dataset externe plus tard pour validation: CSE-CIC-IDS2018, UNSW-NB15, ToN-IoT ou NF-UQ-NIDS-v2.

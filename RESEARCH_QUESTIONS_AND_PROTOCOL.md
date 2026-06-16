# Questions de Recherche et Protocole Experimental - FAIR-ML-CYBER

## Titre de travail

**FAIR-ML-CYBER: A Reproducible and Standardized Framework for Transferability Evaluation in Flow-Based Network Intrusion Detection**

## Objectif scientifique

Evaluer si des modeles ML de detection d'intrusion reseau restent fiables lorsque l'on passe d'une evaluation classique par split aleatoire a des conditions plus proches d'un deploiement:

- futur temporel;
- jour non vu;
- scenario d'attaque non vu;
- endpoint/service non vu;
- attaque inconnue;
- features standardisees et non fuitantes;
- predictions calibrees et explicables.

Contrainte:

> l'etude utilise uniquement le dataset local CICIDS2017-like.

---

## Questions de recherche

### RQ1 - Robustesse des performances

**RQ1. Les performances obtenues avec un split aleatoire restent-elles valides sous des stress-tests temporels, scenario, endpoint et open-set?**

Motivation:

Les scores NIDS sont souvent tres eleves avec un split aleatoire. Mais un split aleatoire peut melanger les memes jours, hotes, services et scenarios entre train et test.

Hypothese:

**H1.** Les performances macro-F1, MCC et PR-AUC diminuent significativement lorsque l'on passe du split aleatoire aux stress-tests.

---

### RQ2 - Portabilite des modeles

**RQ2. Quels modeles conservent la meilleure portabilite entre conditions d'evaluation?**

Motivation:

Un modele qui a le meilleur score en random split n'est pas forcement le plus robuste sous changement temporel ou scenario.

Hypothese:

**H2.** Les modeles a base d'arbres ensembles, comme Random Forest et XGBoost/LightGBM, auront de bons scores en random split, mais leur classement changera sous scenario holdout et endpoint holdout.

Metrique principale:

**Cyber Transferability Score (CTS)**:

`CTS(metric) = metric_stress_test / metric_random_split`

Un score proche de 1 signifie une meilleure portabilite.

---

### RQ3 - Effet des features standardisees

**RQ3. Les features standardisees et non identitaires reduisent-elles la dependance aux artefacts du dataset?**

Motivation:

Des features comme `flow_id`, `timestamp`, `src_ip`, `dst_ip` ou certains ports peuvent encoder le scenario de capture au lieu du comportement reseau.

Hypothese:

**H3.** Les features completes donnent les meilleurs scores en random split, mais les features deployment-safe conservent un meilleur CTS sous stress-tests.

---

### RQ4 - Classes rares

**RQ4. Les attaques rares sont-elles reellement detectees ou masquees par les metriques globales?**

Motivation:

Heartbleed et Web SQL Injection sont tres minoritaires. L'accuracy globale peut etre excellente tout en ratant ces classes.

Hypothese:

**H4.** L'accuracy globale surestime la performance; macro-F1, recall par classe et PR-AUC par classe revelent une detection faible sur les classes rares.

---

### RQ5 - Attaques inconnues et open-set

**RQ5. Un modele entraine en closed-set peut-il identifier une famille d'attaque absente de l'entrainement comme inconnue ou incertaine?**

Motivation:

En production, les attaques futures ne sont pas toutes connues au moment de l'entrainement.

Hypothese:

**H5.** Les classifieurs supervises standards tendent a classer les attaques inconnues comme une classe connue ou comme benign; l'ajout d'un seuil d'incertitude ou d'un detecteur d'anomalie ameliore la detection unknown/review.

---

### RQ6 - Calibration et abstention

**RQ6. La calibration et l'abstention rendent-elles les predictions plus utilisables dans un contexte SOC?**

Motivation:

Un SOC doit prioriser les alertes. Une prediction tres confiante mais fausse est dangereuse.

Hypothese:

**H6.** Les modeles non calibres sont surconfiants sous stress-tests; la calibration et l'abstention reduisent le risque selectif au prix d'une couverture plus faible.

---

### RQ7 - Stabilite des explications

**RQ7. Les features importantes restent-elles stables entre les protocoles d'evaluation?**

Motivation:

Une explication SHAP ou permutation importance n'est utile que si elle reste stable et plausible.

Hypothese:

**H7.** Les explications sont plus instables avec les features completes qu'avec les features deployment-safe.

---

## Variables experimentales

### Variables independantes

1. **Split protocol**
   - random stratified;
   - temporal split;
   - day holdout;
   - scenario holdout;
   - endpoint-pair holdout;
   - service/port holdout;
   - open-set holdout.

2. **Feature tier**
   - full-leaky;
   - no-identity;
   - flow-basic;
   - flow-statistical;
   - deployment-safe.

3. **Model family**
   - Logistic Regression;
   - Random Forest;
   - XGBoost ou LightGBM;
   - MLP;
   - Isolation Forest / Autoencoder pour open-set.

4. **Task**
   - binary classification: Benign vs Attack;
   - multi-class classification: attack label;
   - open-set classification: Benign / Known Attack / Unknown.

### Variables dependantes

- macro-F1;
- weighted-F1;
- MCC;
- balanced accuracy;
- AUROC;
- PR-AUC;
- recall par classe;
- false negative rate par attaque;
- Brier score;
- Expected Calibration Error;
- Cyber Transferability Score;
- inference time;
- top-k explanation stability.

---

## Donnees

### Source

`/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs`

### Taille

- 18 fichiers CSV;
- environ 2.44 millions de flux;
- 122 colonnes;
- 14 labels.

### Labels principaux

- Benign;
- DoS_Hulk;
- DDoS_LOIT;
- Port_Scan;
- FTP-Patator;
- DoS_GoldenEye;
- DoS_Slowhttptest;
- SSH-Patator;
- Botnet_ARES;
- DoS_Slowloris;
- Web_Brute_Force;
- Web_XSS;
- Web_SQL_Injection;
- Heartbleed.

### Preprocessing commun

1. Charger tous les CSV.
2. Ajouter `source_file`.
3. Parser `timestamp`.
4. Nettoyer noms de colonnes.
5. Convertir labels:
   - `binary_label`;
   - `attack_family`.
6. Remplacer `inf`, `-inf`, NaN.
7. Supprimer ou marquer les doublons exacts.
8. Calculer data hash.
9. Sauvegarder en Parquet.

---

## Feature tiers

### Tier 0 - Full-leaky

Toutes les colonnes disponibles.

Usage:

- controle experimental;
- montrer le risque de score gonfle.

### Tier 1 - No-identity

Exclure:

- `flow_id`;
- `timestamp`;
- `src_ip`;
- `dst_ip`.

### Tier 2 - Flow-basic

Garder uniquement:

- protocole;
- duree;
- nombre de paquets;
- nombre de bytes;
- ratio down/up;
- tailles moyennes.

### Tier 3 - Flow-statistical

Inclure:

- payload stats;
- header stats;
- IAT stats;
- flags TCP;
- subflow stats.

### Tier 4 - Deployment-safe

Features non identitaires, plausibles pour un SOC, sans timestamp brut ni IP.

Cette tier est la representation recommandee pour le papier.

---

## Splits experimentaux

### S0 - Random stratified split

Objectif:

- baseline classique.

Configuration:

- train 70%;
- validation 15%;
- test 15%;
- stratification par label.

Analyse:

- mesure de performance optimiste.

---

### S1 - Temporal split

Objectif:

- tester futur temporel.

Configuration possible:

- train: debut de la periode;
- validation: periode intermediaire;
- test: fin de la periode.

Attention:

- certaines attaques sont concentrees sur un seul jour; analyser les labels presents dans chaque split.

---

### S2 - Day holdout

Objectif:

- mesurer portabilite entre jours.

Exemples:

- holdout Tuesday;
- holdout Wednesday;
- holdout Thursday;
- holdout Friday.

Train:

- tous les autres jours.

Test:

- jour holdout.

---

### S3 - Scenario holdout

Objectif:

- mesurer portabilite vers une campagne d'attaque non vue.

Holdouts recommandes:

- Web attacks;
- Botnet_ARES;
- Port_Scan;
- DDoS_LOIT;
- DoS family.

Train:

- benign + autres attaques.

Test:

- benign + attaque holdout.

---

### S4 - Endpoint-pair holdout

Objectif:

- reduire memorisation des communications.

Groupe:

`endpoint_pair = src_ip + dst_ip + dst_port + protocol`

Train/test:

- les groupes ne doivent pas se chevaucher.

---

### S5 - Service/port holdout

Objectif:

- tester robustesse a des services non vus.

Groupe:

`dst_port` ou classe de service.

Train/test:

- certains ports/services uniquement dans test.

---

### S6 - Open-set attack holdout

Objectif:

- simuler attaques inconnues.

Train:

- Benign;
- attaques connues;
- exclure une famille d'attaque.

Test:

- Benign;
- attaques connues;
- famille inconnue.

Sortie:

- benign;
- known attack;
- unknown/review.

---

## Modeles

### Baselines supervises

1. Logistic Regression
2. Random Forest
3. XGBoost ou LightGBM
4. MLP simple

### Modeles open-set/anomaly

1. Isolation Forest
2. One-Class SVM si scalable
3. Autoencoder simple
4. Seuil d'incertitude sur probabilite max
5. Seuil sur entropie

### Regles

- seed fixe;
- meme preprocessing par protocole;
- hyperparametres documentes;
- pas de tuning sur test;
- validation separee;
- MLflow pour chaque run.

---

## Metriques

### Classification binaire

- AUROC;
- PR-AUC;
- F1;
- MCC;
- balanced accuracy;
- false positive rate;
- false negative rate.

### Classification multi-classe

- macro-F1;
- weighted-F1;
- macro precision;
- macro recall;
- MCC multi-classe;
- confusion matrix.

### Classes rares

Rapporter separement:

- Heartbleed;
- Web_SQL_Injection;
- Web_XSS;
- Web_Brute_Force.

Metriques:

- recall;
- precision;
- F1;
- PR-AUC one-vs-rest si possible.

### Portabilite

Cyber Transferability Score:

`CTS_macro_F1 = macro_F1_stress / macro_F1_random`

`CTS_MCC = MCC_stress / MCC_random`

`CTS_PR_AUC = PR_AUC_stress / PR_AUC_random`

### Calibration

- Brier score;
- Expected Calibration Error;
- reliability diagram;
- negative log likelihood.

### Abstention

- coverage;
- selective risk;
- attack recall at coverage;
- unknown detection rate;
- analyst review rate.

### Explicabilite

- top-k feature overlap;
- Spearman rank correlation;
- Kendall tau;
- stability score par split;
- features dominantes par attaque.

### Coût

- training time;
- inference time / 10 000 flows;
- memory usage si possible;
- nombre de features.

---

## Analyses statistiques

### Repetitions

Pour les splits aleatoires:

- 5 seeds minimum;
- rapporter moyenne et ecart-type.

Pour les splits deterministes:

- un split principal;
- variantes si possible.

### Comparaisons

- difference relative entre random et stress-test;
- intervalle de confiance bootstrap sur macro-F1/MCC si possible;
- ranking des modeles par CTS;
- correlation entre nombre de features et robustesse;
- correlation entre calibration et open-set performance.

---

## Figures attendues

### Figure 1 - Architecture FAIR-ML-CYBER

CSV -> preprocessing -> feature tiers -> splits -> models -> MLflow -> metrics/figures.

### Figure 2 - Distribution des labels

Bar chart en log-scale.

### Figure 3 - Timeline des scenarios

Labels par jour et heure.

### Figure 4 - Random split vs stress-tests

Macro-F1/MCC par split.

### Figure 5 - Cyber Transferability Score

Heatmap modeles x splits.

### Figure 6 - Classes rares

Recall/F1 par classe rare.

### Figure 7 - Open-set detection

Known vs unknown performance.

### Figure 8 - Calibration

Reliability diagrams.

### Figure 9 - Explicabilite stable

Top-k feature stability heatmap.

---

## Tables attendues

| Table | Contenu |
|---|---|
| Table 1 | Dataset summary |
| Table 2 | Feature tiers |
| Table 3 | Split protocols |
| Table 4 | Model hyperparameters |
| Table 5 | Main classification results |
| Table 6 | Cyber Transferability Score |
| Table 7 | Rare-class performance |
| Table 8 | Open-set performance |
| Table 9 | Calibration and abstention |
| Table 10 | Runtime and feature cost |

---

## Criteres de succes

Le papier est solide si on obtient:

1. Une difference claire entre random split et stress-tests.
2. Une mesure CTS interpretable.
3. Une demonstration que les feature tiers changent la robustesse.
4. Une analyse credible des classes rares.
5. Une experience open-set coherente.
6. Une calibration/abstention qui ajoute une valeur operationnelle.
7. Une traçabilite complete via hashes, seeds, MLflow.

---

## Menaces a la validite

### Validite interne

- labels potentiellement imparfaits;
- duplication possible;
- preprocessing pouvant influencer les resultats;
- choix des hyperparametres.

### Validite externe

- un seul dataset;
- dataset ancien;
- environnement de capture controle;
- pas de vraie validation sur reseau moderne.

### Validite de construction

- CTS est une metrique proposee, pas encore standard;
- open-set simule par holdout, pas attaque zero-day reelle;
- ports/services peuvent etre des artefacts autant que des signaux utiles.

### Mitigations

- audit explicite;
- protocoles multiples;
- publication des splits;
- reproducibilite MLflow;
- discussion honnete des limites;
- pas de claim excessif.

---

## Ordre recommande des experiences

1. Audit dataset.
2. Random split baseline.
3. Feature tiers sur random split.
4. Temporal split.
5. Day holdout.
6. Scenario holdout.
7. Endpoint holdout.
8. Open-set holdout.
9. Calibration/abstention.
10. Explanation stability.
11. Runtime.

---

## Résumé en une phrase

Le protocole teste si les modeles ML de detection d'intrusion restent fiables quand on retire les conditions faciles du split aleatoire et qu'on mesure leur portabilite, leur calibration, leur comportement face aux attaques rares/inconnues et la stabilite de leurs explications.

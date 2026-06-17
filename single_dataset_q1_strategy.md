# Solution Q1 avec un Seul Dataset

## Decision

On garde uniquement les CSV locaux.  
On change legerement le sujet.

Le papier ne doit pas dire:

> "Nous proposons un nouveau modele ML qui bat l'etat de l'art sur CICIDS2017."

Il doit dire:

> "Nous proposons un cadre de stress-test intra-dataset pour evaluer la fiabilite reelle des modeles NIDS lorsque l'on simule des conditions de deploiement: futur temporel, scenario non vu, endpoints non vus, attaque inconnue, classes rares, calibration et abstention."

C'est la meilleure solution avec un seul dataset.

## Nouveau titre recommande

**From Benchmark Accuracy to Deployment Reliability: A Single-Dataset Stress-Test Framework for Flow-Based Network Intrusion Detection**

Variante plus courte:

**Stress-Testing Flow-Based Intrusion Detection Models Under Temporal, Scenario and Open-Set Shifts**

## Pourquoi ce sujet peut tenir sans dataset externe

Les CSV contiennent deja plusieurs sources naturelles de variation:

- plusieurs jours: 2017-07-03 a 2017-07-07;
- plusieurs campagnes d'attaque: DoS, DDoS, PortScan, Botnet, Brute Force, Web attacks, Heartbleed;
- timestamps precis;
- paires d'hotes et ports;
- classes tres desequilibrees;
- attaques rares;
- labels benign/attack et multi-classe.

Donc on peut construire des tests de robustesse **a l'interieur du dataset**, sans telecharger autre chose.

Ce ne sera pas une validation externe absolue, mais ce sera une evaluation beaucoup plus forte qu'un split aleatoire.

## Contribution centrale

La contribution principale devient:

> un protocole de stress-test reproductible pour NIDS flow-based construit a partir d'un seul dataset labellise, montrant comment les performances changent lorsque l'on passe d'une evaluation random classique a des conditions plus proches du deploiement.

Etat empirique au 2026-06-17:

- le protocole core est execute en full-data dans `fullcore-mem-s42-001` et `fullcore-mem-s7-001`;
- chaque run utilise 2,438,052 lignes, 2 feature tiers, 5 splits, 2 modeles, 20/20 runs completes;
- HistGradientBoosting atteint une macro-F1 moyenne multi-seed de 0.9978 en random split, mais seulement 0.2322 en temporal et 0.3988 en day-holdout;
- LogisticRegression atteint 0.9360 en random split, puis 0.5401 en temporal et 0.6386 en day-holdout;
- ce resultat concret soutient la contribution, mais le papier doit encore ajouter open-set, rare-class, calibration/abstention et analyses de stabilite pour viser Q1.

## Contributions acceptables pour Q1

### C1 - Reliability stress-test suite

Creer une suite de splits:

| Split | Idee | Valeur scientifique |
|---|---|---|
| Random stratified | baseline classique | montre le score optimiste |
| Temporal future split | train sur passe, test sur futur | simule deploiement temporel |
| Day holdout | un jour entier en test | simule changement de contexte |
| Scenario holdout | une campagne d'attaque absente du train | simule attaque non vue |
| Endpoint-pair holdout | paires IP/port separees entre train/test | reduit memorisation |
| Service/port holdout | certains ports/services en test | teste robustesse protocolaire |
| Rare-attack stress test | Heartbleed, SQL Injection, XSS | verifie classes minoritaires |
| Open-set family holdout | famille d'attaque inconnue | detecte inconnu / abstention |

### C2 - Leakage sensitivity analysis

Tester l'impact des colonnes potentiellement dangereuses:

- avec/sans `flow_id`;
- avec/sans `timestamp`;
- avec/sans `src_ip`, `dst_ip`;
- avec/sans ports;
- full features vs features operationnelles.

Objectif:

> montrer si le modele apprend le comportement reseau ou des artefacts du scenario.

### C3 - Rare-attack reliability

Les classes Heartbleed et Web_SQL_Injection sont minuscules. L'article doit refuser l'accuracy globale comme metrique principale.

Mesurer:

- macro-F1;
- balanced accuracy;
- MCC;
- recall par classe;
- PR-AUC par classe;
- false negative rate par attaque.

### C4 - Open-set and abstention

Comme on n'a pas d'autre dataset, on simule les attaques inconnues:

- retirer une famille du train;
- entrainer sur attaques connues;
- tester sur attaques connues + famille inconnue;
- utiliser seuil d'incertitude, entropy, conformal prediction ou calibration.

Sorties:

- known attack;
- benign;
- unknown/review.

Cette contribution est plus forte qu'une classification multi-classe standard.

### C5 - Calibration for SOC use

Un SOC ne veut pas seulement une classe; il veut savoir si l'alerte est fiable.

Mesurer:

- Brier score;
- Expected Calibration Error;
- reliability curves;
- coverage-risk curve;
- taux d'abstention;
- taux d'alertes transferees a un analyste.

### C6 - Explanation stability

Utiliser SHAP ou permutation importance, mais avec une vraie question:

> les features explicatives restent-elles les memes quand le split change?

Mesurer:

- overlap top-k features entre splits;
- Kendall/Spearman rank correlation;
- stabilite par famille d'attaque;
- difference random split vs temporal/scenario split.

## Modele scientifique du papier

### Question principale

**RQ1.** Les performances annoncees par split aleatoire restent-elles valides sous stress-tests temporels, scenario, endpoint et open-set?

### Questions secondaires

**RQ2.** Quelles features causent le plus de fuite ou de memorisation?

**RQ3.** Les attaques rares sont-elles reellement detectees ou masquees par l'accuracy globale?

**RQ4.** L'abstention/calibration peut-elle rendre le modele plus utilisable en SOC?

**RQ5.** Les explications du modele sont-elles stables sous changement de protocole?

## Modeles a utiliser

Pas besoin d'inventer une architecture trop complexe. Il faut des baselines solides:

- Logistic Regression;
- Random Forest;
- XGBoost ou LightGBM;
- MLP simple;
- Isolation Forest ou Autoencoder pour open-set.

Le papier doit montrer que le protocole change les conclusions, pas seulement que XGBoost est fort.

## Resultats attendus

On s'attend a voir:

- scores tres hauts en split aleatoire;
- chute sous temporal/day/scenario holdout;
- forte fragilite des classes rares;
- instabilite des explications si les features de contexte sont incluses;
- meilleure credibilite quand les features fuiteuses sont retirees;
- abstention utile pour reduire les predictions dangereuses.

## Ce qui rend le papier defendable en Q1

Avec un seul dataset, la defense doit etre:

1. **On ne pretend pas prouver la generalisation universelle.**
2. **On propose une methode pour eviter les conclusions trompeuses sur un benchmark tres utilise.**
3. **On fournit un protocole reutilisable pour d'autres datasets.**
4. **On montre empiriquement que les choix de split/features changent radicalement les conclusions.**
5. **On produit un benchmark reproductible, auditable, utile aux chercheurs et SOC.**

## Ce qu'il ne faut pas faire

Ne pas centrer l'article sur:

- "nouveau deep learning model";
- accuracy globale;
- comparaison superficielle de 10 classifieurs;
- SMOTE + Random Forest + 99%;
- claim de zero-day reel sans validation externe.

## Structure finale conseillee

1. Introduction
   - probleme des scores trop optimistes en NIDS;
   - besoin d'evaluation fiable avec donnees limitees.

2. Related Work
   - CICIDS2017;
   - limites connues;
   - generalisation NIDS;
   - open-set detection;
   - calibration/XAI.

3. Dataset Audit
   - 2.44M flux;
   - 14 labels;
   - desequilibre extreme;
   - jours/scenarios;
   - features potentiellement fuiteuses.

4. Stress-Test Framework
   - splits;
   - feature tiers;
   - modeles;
   - metriques.

5. Results
   - random vs robust splits;
   - rare classes;
   - open-set;
   - calibration;
   - explanation stability;
   - runtime.

6. Discussion
   - que valent les scores CICIDS2017;
   - recommandations;
   - limites single-dataset.

7. Conclusion
   - framework reproductible.

## Cible journal recommandee

Avec un seul dataset, la cible la plus realiste reste:

**Computers & Security**

Deuxieme option:

**Expert Systems with Applications**

IEEE TDSC / TIFS restent trop ambitieux sans validation externe ou contribution algorithmique majeure.

## Verdict final

Oui, il existe une solution avec ces donnees uniquement:

> faire un article sur la fiabilite des evaluations ML pour NIDS via un stress-test intra-dataset complet.

Ce n'est pas garanti Q1, mais c'est la forme la plus defendable pour viser Q1 avec un seul dataset.

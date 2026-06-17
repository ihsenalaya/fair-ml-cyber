# Revue Critique Q1 - FAIR-ML-CYBER

Date: 2026-06-17

## Décision simulée

**Major Revision.**

Le travail est devenu sérieux et défendable, mais il n'est pas encore prêt pour une soumission Q1 sans renforcement. La contribution doit être présentée comme une étude de validité des benchmarks et de fiabilité en déploiement, pas comme un nouveau détecteur d'intrusion qui bat l'état de l'art.

## Verdict court

Le projet a maintenant une base empirique réelle:

- dataset complet: 2,438,052 flux;
- core binaire validé sur seeds 42, 7 et 99;
- rerun LogisticRegression seed 42 sans warning de convergence;
- run avancé seed 42 avec rare-class, multi-class, open-set, calibration/abstention et stabilité d'explications;
- preuves traçables dans `evidence/` et journal d'expérience.

Cependant, un reviewer Q1 exigera plus de robustesse statistique et méthodologique avant d'accepter.

## Forces du papier

1. **Traçabilité expérimentale forte.** Les runs Azure, les hashes, les seeds, les chemins d'artefacts et les warnings sont documentés.

2. **Signal scientifique clair.** Les scores random split sont très élevés, mais temporal/day/scenario stress-tests montrent une chute nette. Cela soutient l'angle "benchmark accuracy vs deployment reliability".

3. **Résultats full-data réels.** Les résultats principaux ne sont plus des smoke tests. Les runs core utilisent les 2,438,052 lignes.

4. **Analyses avancées pertinentes.** Le run `advanced-core-s42-001` montre que les résultats binaires cachent des faiblesses multi-class, rare-class, open-set, calibration et explication.

5. **Positionnement compatible Q1.** La meilleure cible reste Computers & Security, avec un cadrage data-centric/evaluation-centric.

## Critiques majeures

### 1. Dataset unique et ancien

Le dataset ressemble fortement à CICIDS2017 ou une variante CICIDS2017-like. C'est un benchmark ancien, très utilisé et déjà critiqué. Un reviewer peut dire que la contribution empirique est limitée par l'absence de validation externe.

**Risque:** rejet si le papier ressemble à une nouvelle comparaison de modèles sur CICIDS2017.

**Correction:** assumer explicitement que l'article est une étude de validité intra-dataset et de stress-test, pas une preuve de généralisation universelle.

### 2. Analyses avancées seulement sur seed 42

Le core binaire est multi-seed, mais les analyses rare-class, multi-class, open-set, calibration/abstention et stabilité d'explications ne sont validées que sur seed 42.

**Risque:** les conclusions avancées peuvent être vues comme exploratoires.

**Correction prioritaire:** relancer `advanced-core` sur seeds 7 et 99, ou limiter les claims avancés à une analyse seed 42.

### 3. Convergence LogisticRegression incomplète en multi-seed

Le rerun `fullcore-lr2000-s42-001` corrige la convergence pour seed 42. Mais les anciens runs seed 7 et 99 gardent les warnings `max_iter=500`.

**Risque:** les tables LR multi-seed peuvent être contestées.

**Correction prioritaire:** relancer LR2000 pour seeds 7 et 99, ou exclure les anciennes lignes LR warning-bearing des tables finales.

### 4. Open-set trop simple

L'open-set actuel repose sur l'incertitude d'un classifieur fermé. C'est utile pour montrer une limite, mais ce n'est pas une méthode open-set forte.

Résultat vérifié: LR échoue pour DDoS uncertainty AUROC 0.2019, alors que HGB atteint 0.9954 sur PortScan.

**Risque:** un reviewer demandera des baselines open-set plus sérieuses.

**Correction:** ajouter au moins une baseline anomaly/open-set: Isolation Forest, One-Class SVM, autoencoder simple, energy score ou conformal prediction.

### 5. Calibration mesurée mais pas corrigée

Les résultats montrent une forte dégradation de calibration:

- HGB temporal ECE: 0.7013;
- LR temporal ECE: 0.3955.

**Risque:** le papier démontre un problème mais ne propose pas de réponse méthodologique suffisante.

**Correction:** ajouter Platt scaling, isotonic regression ou temperature scaling, puis comparer ECE/Brier avant/après calibration.

### 6. Explicabilité encore légère

La stabilité top-15 est intéressante:

- HGB temporal Jaccard: 0.0714;
- LR temporal Jaccard: 0.5789.

Mais l'importance HGB utilise seulement 2,000 exemples et une répétition de permutation.

**Risque:** l'analyse XAI peut être jugée fragile.

**Correction:** augmenter les répétitions, ajouter bootstrap, mesurer stabilité par seed et discuter la plausibilité opérationnelle des features dominantes.

### 7. Classes rares: résultats à cadrer comme échec contrôlé

En Web holdout, les classes Web rares ont F1 0.0 malgré supports non nuls:

- `Web_Brute_Force`: support 2,734;
- `Web_SQL_Injection`: support 24;
- `Web_XSS`: support 1,358.

**Risque:** si le papier prétend détecter les classes rares, il sera attaqué.

**Correction:** présenter cela comme une preuve que les métriques globales masquent l'échec rare-class.

### 8. Absence d'intervalles de confiance

Les résultats sont solides mais les tables ne donnent pas encore d'incertitude statistique.

**Correction prioritaire:**

- bootstrap confidence intervals pour macro-F1, AUROC, AUPRC, ECE;
- paired bootstrap random vs temporal;
- CI par classe rare quand le support le permet;
- analyse de sensibilité des seuils d'abstention.

### 9. Endpoint-pair holdout peu discriminant

Endpoint-pair holdout reste très élevé, notamment HGB CTS proche de 1.

**Risque:** le reviewer peut conclure que ce split ne teste pas réellement la généralisation.

**Correction:** expliquer ce résultat comme une observation empirique, pas comme preuve de robustesse. Ajouter si possible service/port holdout.

## Recommandations avant soumission Q1

Priorité 1:

1. Relancer `advanced-core` sur seeds 7 et 99.
2. Relancer LR2000 sur seeds 7 et 99.
3. Ajouter calibration post-hoc.
4. Ajouter au moins une baseline open-set/anomaly.
5. Ajouter intervalles de confiance et tests bootstrap.

Priorité 2:

1. Renforcer l'analyse XAI avec plus de répétitions.
2. Ajouter service/port holdout si faisable.
3. Construire les figures publication-ready.
4. Nettoyer les claims pour éviter toute promesse de SOTA.

## Cible journal

La cible la plus réaliste est **Computers & Security**.

Expert Systems with Applications devient possible si la partie calibration/XAI/open-set est renforcée.

IEEE TDSC ou IEEE TIFS restent très difficiles avec un seul dataset et sans contribution algorithmique nouvelle.

## Conclusion reviewer

Le papier a un vrai potentiel Q1, mais seulement s'il assume son angle:

> une étude reproductible et critique de la fiabilité des évaluations NIDS sous stress-tests de déploiement.

Il ne doit pas être vendu comme:

> un nouveau modèle de détection d'intrusion atteignant de meilleurs scores.

Le résultat le plus fort n'est pas "nous détectons mieux". Le résultat fort est:

> les scores classiques sont trompeurs; la portabilité, la calibration, les classes rares, l'open-set et les explications changent radicalement sous stress-tests.

Décision simulée finale: **Major Revision, potentiellement acceptable après renforcement expérimental.**

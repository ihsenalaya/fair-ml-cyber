# Verification de Faisabilite Q1

Date de verification: 2026-06-16.

## Verdict net

**Non, on ne peut pas etre sur que ces donnees donnent un article Q1.**

Avec les CSV seuls, si l'article se limite a entrainer des modeles ML sur CICIDS2017-like et rapporter accuracy/F1, la probabilite Q1 est **faible**.

Une soumission Q1 devient plausible seulement si l'article apporte une contribution plus forte:

- audit methodologique du dataset;
- protocole anti-fuite;
- evaluation temporelle et scenario-holdout;
- open-set / unknown attack detection;
- calibration et abstention;
- explicabilite stable;
- idealement validation externe sur un deuxieme dataset.

Mise a jour empirique au 2026-06-17:

- les runs full-data core `fullcore-mem-s42-001` et `fullcore-mem-s7-001` sont termines sur les 2,438,052 lignes, chacun avec 20/20 runs completes et 0 echec;
- les resultats confirment sur deux seeds une forte rupture entre `random_stratified` et les stress-tests temporel/day/scenario;
- ce signal renforce la these "benchmark accuracy vs deployment reliability";
- cela ne suffit toujours pas a garantir Q1: il manque rare-class/multi-class, open-set, calibration/abstention et stabilite d'explications.

## Pourquoi le risque est eleve

### 1. CICIDS2017 est tres utilise et ancien

Les fichiers locaux correspondent tres fortement a CICIDS2017 ou une variante derivee. CICIDS2017 reste utile, mais il est massivement utilise depuis 2017-2018. Un papier "nouveau modele + CICIDS2017" est difficile a vendre en Q1.

Source: page officielle CICIDS2017, Canadian Institute for Cybersecurity:  
https://www.unb.ca/cic/datasets/ids-2017.html

### 2. La qualite de CICIDS2017 est critiquee

Engelen, Rimmer et Joosen ont montre des problemes de generation de trafic, construction de flows, extraction de features et labels. Leur papier indique que plus de 20% des traces originales ont ete reconstruites ou relabelisees dans leur version corrigee.

Source:  
https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf

### 3. Les modeles NIDS generalisent mal

Des travaux recents montrent que les scores quasi parfaits intra-dataset peuvent s'effondrer en cross-dataset. L'etude de Cantone et al. utilise CIC-IDS2017, CSE-CIC-IDS2018 et des variantes LycoS; elle rapporte des performances presque parfaites sur le meme dataset mais proches du hasard dans plusieurs configurations cross-dataset.

Source:  
https://arxiv.org/abs/2402.10974

### 4. Les surveys recents demandent de la rigueur dataset

Le survey Computers & Security 2025 sur 89 datasets NIDS insiste sur les limites de selection, qualite et usage des datasets. Cela confirme que la contribution acceptable aujourd'hui doit etre plus data-centric et reproductible qu'un simple benchmark de modeles.

Source:  
https://doi.org/10.1016/j.cose.2025.104510  
Version arXiv: https://arxiv.org/abs/2502.06688

## Verification des journaux Q1

Les journaux Q1 existent bien pour ce sujet:

| Journal | Statut verifie | Faisabilite avec ce projet |
|---|---|---|
| Computers & Security | JCR Q1, IF 2025 autour de 5.4 selon Journal Metrics | Cible la plus realiste si l'article est methodologique et rigoureux |
| Expert Systems with Applications | JCR Q1, IF 2025 autour de 7.5 selon Journal Metrics | Possible si contribution ML/XAI forte et experiments solides |
| IEEE TDSC | SJR/JCR Q1 selon sources de ranking | Tres difficile avec un seul dataset ancien |
| IEEE TIFS | SJR/JCR Q1, scope information security/forensics | Peu probable sans vraie nouveaute algorithmique ou systeme tres fort |

Sources:

- Computers & Security: https://www.journalmetrics.org/journal/computers-and-security
- Expert Systems with Applications: https://www.journalmetrics.org/journal/expert-systems-with-applications
- IEEE TIFS scope: https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security/ieee-transactions
- SCImago Computers & Security: https://www.scimagojr.com/journalsearch.php?q=28898&tip=sid
- SCImago IEEE TDSC: https://www.scimagojr.com/journalsearch.php?clean=0&q=28918&tip=sid
- SCImago IEEE TIFS: https://www.scimagojr.com/journalsearch.php?clean=0&q=4000149002&tip=sid

## Probabilite estimee par scenario

| Scenario d'article | Probabilite Q1 |
|---|---|
| Simple comparaison RF/XGBoost/MLP sur ces CSV | Faible |
| Nouveau modele deep learning sur ces CSV uniquement | Faible a moyenne-faible |
| Benchmark anti-fuite + temporel + open-set + calibration + XAI sur ces CSV | Moyenne pour Computers & Security / ESWA |
| Meme benchmark + validation externe CSE-CIC-IDS2018 ou UNSW-NB15/ToN-IoT | Moyenne a bonne |
| Nouvelle methode algorithmique robuste + multi-dataset + code reproductible | Bonne pour Computers & Security / ESWA, possible pour IEEE selon niveau |

## Decision recommandee

Pour viser Q1 serieusement, il faut renforcer la proposition:

1. Ne pas se limiter aux CSV locaux.
2. Ajouter au moins un dataset externe: CSE-CIC-IDS2018, UNSW-NB15, ToN-IoT ou NF-UQ-NIDS-v2.
3. Faire une contribution experimentale claire:
   - random split vs temporal split;
   - scenario holdout;
   - endpoint holdout;
   - open-set attack holdout;
   - calibration/abstention;
   - SHAP stability.
4. Publier code, configs, seeds, splits et scripts.

## Conclusion

**Ces donnees peuvent servir de base a un article Q1, mais elles ne suffisent pas seules.**

Le chemin Q1 realiste est:

> un papier de benchmark robuste et reproductible sur les limites des evaluations ML pour NIDS, idealement avec validation externe multi-dataset.

Le chemin non-Q1 est:

> un papier classique de classification CICIDS2017 avec accuracy elevee.

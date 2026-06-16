# Etat de l'Art et Bibliographie - FAIR-ML-CYBER

## Sujet scientifique retenu

**FAIR-ML-CYBER: A Reproducible and Standardized Framework for Transferability Evaluation in Flow-Based Network Intrusion Detection**

L'article vise a adapter l'idee de FAIR-ML-ICU a la detection d'intrusion reseau:

- standardiser les features de flux reseau;
- tracer les experiences ML;
- mesurer la reproductibilite;
- mesurer la portabilite des modeles entre jours, scenarios, services et attaques non vues;
- eviter les scores artificiellement gonfles par des splits aleatoires ou des artefacts de dataset.

Le dataset local ressemble fortement a **CICIDS2017** ou a une variante derivee: flux reseau, timestamps 2017-07-03 a 2017-07-07, labels `Benign`, `DoS_Hulk`, `DDoS_LOIT`, `Port_Scan`, `Botnet_ARES`, `FTP-Patator`, `SSH-Patator`, `Web_XSS`, `Heartbleed`, etc.

---

## Synthese courte

La litterature montre quatre constats utiles pour positionner FAIR-ML-CYBER:

1. **CICIDS2017 est un benchmark tres utilise**, mais il est ancien et plusieurs travaux ont identifie des problemes de labellisation, de generation de flux et d'extraction de features.
2. **Les performances NIDS intra-dataset sont souvent trop optimistes**, surtout avec des splits aleatoires qui melangent jours, hotes, services et scenarios.
3. **La generalisation est le vrai probleme scientifique**, mais elle est rarement mesuree correctement. Les travaux cross-dataset montrent souvent une chute massive de performance.
4. **Les features standardisees, la reproductibilite, l'incertitude, l'open-set detection et l'explicabilite** sont des axes actuels qui permettent de transformer un papier CICIDS2017 classique en contribution plus forte.

Positionnement propose:

> FAIR-ML-CYBER ne cherche pas seulement a battre un score sur CICIDS2017. Il propose un cadre reproductible pour mesurer la portabilite et la fiabilite des modeles ML de detection d'intrusion quand on impose des stress-tests temporels, scenario, endpoint, service et open-set.

---

## Axe 1 - Datasets NIDS et CICIDS2017

### Reference centrale: CICIDS2017

**Sharafaldin, Lashkari, Ghorbani (2018)** introduisent CICIDS2017. Le dataset vise a fournir du trafic benin et des attaques courantes sous forme PCAP et CSV de flux extraits par CICFlowMeter. La page officielle UNB precise que les CSV sont labellises a partir des timestamps, IPs source/destination, ports, protocoles et type d'attaque.

Role pour notre article:

- justifier l'usage du dataset local;
- decrire les scenarios d'attaque;
- expliquer la nature flow-based des donnees.

Limite:

- l'article original presente CICIDS2017 comme un benchmark plus realiste, mais des travaux ulterieurs ont documente ses problemes.

Sources:

- CICIDS2017 official page: https://www.unb.ca/cic/datasets/ids-2017.html
- Sharafaldin et al. 2018: https://www.scitepress.org/papers/2018/66398/66398.pdf

### Surveys sur datasets NIDS

**Ring et al. (2019)** proposent une revue des datasets de detection d'intrusion reseau et identifient des proprietes pour evaluer leur adequation: volume, environnement de capture, types de donnees, labellisation, metadonnees, actualite, etc.

**Goldschmidt et Chuda (2025)** etendent cette logique avec une revue systematique de 89 datasets publics pour NIDS, en discutant les limites recurrentes: qualite, representativite, popularite excessive de certains benchmarks, choix de dataset mal justifies.

Role pour notre article:

- justifier un audit dataset avant toute modelisation;
- montrer que la qualite du dataset est une question scientifique centrale;
- positionner FAIR-ML-CYBER comme framework de selection/evaluation, pas seulement comme modele.

Sources:

- Ring et al. 2019: https://doi.org/10.1016/j.cose.2019.06.005
- Goldschmidt et Chuda 2025: https://arxiv.org/abs/2502.06688

---

## Axe 2 - Limites connues de CICIDS2017

### Troubleshooting CICIDS2017

**Engelen, Rimmer, Joosen (2021)** revisitent CICIDS2017 et analysent sa chaine de generation: trafic, construction des flows, extraction des features et labelling. Ils identifient des problemes affectant la validite du dataset et proposent une methodologie de correction. Leur papier indique que plus de 20% des traces originales ont ete reconstruites ou relabelisees.

Role pour notre article:

- argument fort pour ne pas faire un papier naif "99% accuracy";
- justifier un audit de qualite des donnees;
- justifier des experiments de sensibilite aux features et aux splits.

Source:

- https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf

### Analyse LycoSTand / LYCOS-IDS2017

**Rosay et al. (2022)** analysent CICIDS2017 en detail et rapportent des problemes dans les flows extraits des paquets reseau. Ils proposent LycoSTand, un outil alternatif d'extraction de flux, et produisent LYCOS-IDS2017.

Role pour notre article:

- montrer que les features de flux ne sont pas neutres;
- motiver notre separation entre "features completes", "features potentiellement fuitantes" et "features standardisees/deployment-safe";
- soutenir l'idee que la representation des donnees influence fortement les conclusions ML.

Sources:

- https://www.scitepress.org/Papers/2022/107740/107740.pdf
- DOI: https://doi.org/10.5220/0010774000003120

### Erreurs de labellisation et ecarts de performance

Des travaux supplementaires signalent des erreurs dans CICIDS2017 et montrent que les corrections peuvent changer fortement les performances mesurees.

Role pour notre article:

- renforcer la section "Threats to validity";
- eviter toute conclusion excessive sur la detection d'attaques rares;
- justifier le logging des hashes, splits et configs.

Sources:

- https://hal.science/hal-03775466v1/document
- https://dl.acm.org/doi/10.1007/978-3-031-31108-6_2

---

## Axe 3 - Evaluation ML pour NIDS: du score au deploiement

### Probleme des evaluations trop academiques

**Sommer et Paxson (2010)** restent une reference fondamentale. Ils expliquent pourquoi la detection d'intrusion est un probleme difficile pour le ML: rarete des attaques, cout des faux positifs, non-stationnarite, comportement adversarial, distance entre benchmark et deploiement.

**Apruzzese, Laskov, Schneider (2023)** proposent une evaluation pragmatique du ML pour NIDS. Ils critiquent la tendance a montrer qu'une nouvelle methode "outperform" les precedentes sans evaluer les implications operationnelles: cout, materiel, scenarios adversariaux, conditions de deploiement.

**Apruzzese (2026)** poursuit cette critique avec un SoK sur la necessite de reshaper la recherche NIDS, en particulier parce que les papiers academiques se traduisent mal en contexte operationnel.

Role pour notre article:

- justifier les metriques de deploiement: temps d'inference, abstention, calibration;
- justifier que l'accuracy ne suffit pas;
- positionner FAIR-ML-CYBER comme evaluation-oriented et deployment-aware.

Sources:

- Sommer et Paxson 2010: https://doi.org/10.1109/SP.2010.25
- Apruzzese et al. 2023: https://arxiv.org/abs/2305.00550
- Apruzzese 2026: https://arxiv.org/abs/2604.17556

### Barriere entre recherche et utilisateurs SOC

**Dietz et al. (2026)** analysent les obstacles d'adoption des IDS bases sur IA/ML du point de vue des utilisateurs. Les dimensions importantes incluent: adequation des donnees, reproductibilite, explicabilite, praticabilite, utilisabilite et confidentialite.

Role pour notre article:

- soutenir l'ajout de MLflow, data hash, feature hash, split hash;
- justifier la dimension "SOC-usable";
- justifier calibration, abstention et explications stables.

Source:

- https://opus.bibliothek.uni-augsburg.de/opus4/files/113828/The_Missing_Link_in_Network_Intrusion_Detection_Taking_AI_ML_Research_Efforts_to_Users.pdf

---

## Axe 4 - Standardisation des features et generalisation

### Features NetFlow standardisees

**Sarhan, Layeghy, Portmann (2021)** soutiennent qu'un probleme majeur des datasets NIDS est l'absence d'un feature set commun. Chaque dataset utilise des features proprietaires ou specifiques, ce qui empeche les comparaisons fiables et limite l'etude de la generalisation. Ils proposent des feature sets NetFlow de 12 et 43 features.

**Sarhan, Layeghy, Portmann (2022)** evaluent des feature sets standardises pour ameliorer generalisabilite et explicabilite sur plusieurs datasets. Ils comparent notamment NetFlow et CICFlowMeter, et utilisent SHAP pour analyser l'influence des features.

Role pour notre article:

- c'est l'equivalent cyber de FHIR/LOINC dans FAIR-ML-ICU;
- justifier les "feature tiers" dans FAIR-ML-CYBER;
- proposer une representation "deployment-safe" plus portable que les 122 features brutes.

Sources:

- https://arxiv.org/abs/2101.11315
- https://doi.org/10.1007/s11036-021-01843-0
- https://arxiv.org/abs/2104.07183
- https://doi.org/10.1016/j.bdr.2022.100359

### Generalisation cross-dataset

**Cantone, Marrocco, Bria (2024)** montrent que les modeles NIDS peuvent atteindre des performances presque parfaites quand train et test viennent du meme dataset, mais chuter vers des performances proches du hasard dans plusieurs configurations cross-dataset. Le papier met en avant l'heterogeneite des donnees et les anomalies de dataset comme obstacles a la generalisation.

Role pour notre article:

- meme si nous n'avons pas de deuxieme dataset, ce papier justifie la question de portabilite;
- notre solution single-dataset devient: construire des stress-tests internes qui approchent la logique cross-domain;
- utiliser `CTS = metric_target / metric_source` comme proxy de transferabilite.

Sources:

- https://arxiv.org/abs/2402.10974
- DOI: https://doi.org/10.1109/ACCESS.2024.3472907

---

## Axe 5 - Splits, fuites et protocoles temporels

Un probleme recurrent des papiers NIDS est le split aleatoire. Dans des donnees de flux capturees par jour/scenario, un split aleatoire peut mettre dans train et test:

- les memes hotes;
- les memes services;
- les memes patterns temporels;
- des duplicats ou quasi-duplicats;
- des flows issus de la meme campagne d'attaque.

Cela peut gonfler les scores.

Des travaux recents sur CICIDS2017 et les modeles temporels montrent que la methodologie d'evaluation peut avoir plus d'impact que l'architecture du modele. Par exemple, certains resultats indiquent que des splits "leakage-free" et des conventions de padding explicites changent fortement la performance des architectures sequence.

Role pour notre article:

- faire de la suite de splits le coeur de la contribution;
- comparer random split, temporal split, day holdout, scenario holdout, endpoint holdout, service holdout, open-set holdout;
- mesurer la degradation par `Cyber Transferability Score`.

Source recente utile:

- Moczkodan et Ragab 2026: https://arxiv.org/abs/2606.11098

Note:

- cette reference est recente et preprint; elle doit etre utilisee prudemment, mais elle renforce directement notre positionnement.

---

## Axe 6 - Open-set et attaques inconnues

La majorite des modeles NIDS sont entraines en **closed set**: toutes les classes vues au test sont supposees connues pendant l'entrainement. Or, en contexte cyber, une attaque inconnue est plausible.

Des travaux sur l'open-set intrusion detection utilisent OpenMax, energie, autoencodeurs, detection d'anomalies ou combinaisons de classifieurs fermes et detecteurs inconnus. Les resultats montrent souvent un compromis: detecter l'inconnu peut augmenter les faux positifs ou reduire la precision sur classes connues.

Role pour notre article:

- simuler l'open-set avec un seul dataset en retirant une famille d'attaque du train;
- evaluer si le modele classe l'inconnu comme benign, known attack ou unknown/review;
- ajouter une option d'abstention SOC.

Sources:

- Unknown intrusion traffic detection, Scientific Reports 2025: https://www.nature.com/articles/s41598-025-01084-1
- Open-set energy-based flow classifier: https://arxiv.org/html/2109.11224v3
- Unknown network attack detection with open set recognition: https://www.researchgate.net/publication/343241148_Unknown_Network_Attack_Detection_Based_on_Open_Set_Recognition

---

## Axe 7 - Calibration, incertitude et abstention

Les modeles ML peuvent etre surconfiants, notamment sur des attaques inconnues ou des donnees hors distribution. En NIDS, cela a un impact operationnel direct: faux positifs, fatigue des analystes, faux negatifs critiques.

Des travaux recents insistent sur l'importance de l'incertitude pour des IDS plus fiables. Les metriques utiles sont:

- Brier score;
- Expected Calibration Error;
- reliability diagram;
- negative log likelihood;
- coverage-risk curve;
- selective risk.

Role pour notre article:

- transformer le modele en systeme utilisable par un SOC;
- ne pas seulement dire "classe A", mais fournir "classe A avec confiance calibree" ou "unknown/review";
- introduire un compromis entre couverture automatique et recours analyste.

Sources:

- Talpini et al. 2024, trustworthiness with uncertainty quantification: https://link.springer.com/article/10.1007/s40860-024-00238-8
- Calibration techniques for IDS, 2025: https://csit.am/2025/proceedings/TN/TN_1.pdf
- Selective classification benchmarks: https://data.mlr.press/assets/pdf/v01-17.pdf

---

## Axe 8 - Explicabilite et stabilite des explications

La litterature XAI pour IDS utilise souvent SHAP ou LIME. Le probleme est que beaucoup de papiers se limitent a montrer un graphe d'importance de features sans tester si les explications sont stables entre splits, scenarios ou representations.

Pour FAIR-ML-CYBER, la question interessante est:

> les features les plus importantes restent-elles les memes quand on passe du random split au temporal/scenario/endpoint holdout?

Role pour notre article:

- utiliser permutation importance ou SHAP;
- mesurer top-k overlap et correlations de rang;
- identifier si le modele depend de features operationnelles ou d'artefacts.

Sources:

- Sarhan et al. 2022, SHAP + feature standardization: https://arxiv.org/abs/2104.07183
- Mohale et Obagbuwa 2025, XAI for IDS: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1520741/full

---

## Axe 9 - Reproductibilite et traçabilite experimentale

La reproductibilite est un probleme transversal en ML. Les travaux generaux sur la reproductibilite soulignent des barrieres: manque de code, seeds absentes, preprocessing non documente, splits non publies, hyperparametres incomplets.

Role pour notre article:

- reprendre la logique FAIR-ML-ICU:
  - data hash;
  - feature hash;
  - split hash;
  - seed;
  - MLflow run ID;
  - params;
  - metrics;
  - runtime;
  - versions de packages;
- faire de la reproductibilite une partie de la contribution.

Sources:

- Reproducibility in ML-based research, 2024: https://arxiv.org/html/2406.14325v3
- MLflow, tracking metrics and artifacts: https://azure.microsoft.com/en-us/blog/make-your-data-science-workflow-efficient-and-reproducible-with-mlflow/

---

## Gap scientifique final

La litterature contient:

- beaucoup de modeles ML/DL sur CICIDS2017;
- des critiques fortes sur CICIDS2017;
- des travaux sur features standardisees;
- des travaux sur generalisation cross-dataset;
- des travaux sur open-set, calibration, XAI.

Mais il manque encore un cadre simple et reproductible qui combine, sur un dataset flow-based tres utilise:

1. audit de qualite;
2. feature tiers standardises;
3. stress-tests intra-dataset;
4. mesure de portabilite;
5. calibration/abstention;
6. explicabilite stable;
7. traçabilite MLflow/hash/seed.

Formulation du gap:

> Existing CICIDS2017-based studies mostly optimize model performance under conventional evaluation protocols. There is limited work that systematically measures how model conclusions change under leakage-aware, temporal, scenario, endpoint and open-set stress-tests while preserving reproducibility and feature-set traceability.

---

## Contribution proposee apres l'etat de l'art

FAIR-ML-CYBER apporte:

1. **Framework reproductible** pour NIDS flow-based.
2. **Feature standardization tiers**, inspiree des travaux NetFlow.
3. **Cyber Transferability Score**, pour mesurer la chute de performance sous stress-test.
4. **Suite de splits anti-fuite**, adaptee a un seul dataset.
5. **Evaluation rare-class et open-set**, utile pour attaques minoritaires et inconnues.
6. **Calibration/abstention**, pour un usage SOC.
7. **Explanation stability**, pour verifier si les explications sont robustes.

---

## Bibliographie prioritaire annotee

### B1. Dataset et fondations

1. **Sharafaldin, I., Lashkari, A. H., Ghorbani, A. A. (2018). Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. ICISSP.**  
   Reference fondatrice de CICIDS2017. A citer pour decrire le dataset et les scenarios.

2. **Canadian Institute for Cybersecurity. CICIDS2017 official dataset page.**  
   Source officielle pour PCAP/CSV, labels et description du dataset.

3. **Ring, M., Wunderlich, S., Scheuring, D., Landes, D., Hotho, A. (2019). A Survey of Network-based Intrusion Detection Data Sets. Computers & Security.**  
   Reference solide pour discuter le choix et les proprietes des datasets NIDS.

4. **Goldschmidt, P., Chuda, D. (2025). Network Intrusion Datasets: A Survey, Limitations, and Recommendations. Computers & Security / arXiv.**  
   Reference recente pour montrer que la question dataset reste centrale en 2025.

### B2. Limites CICIDS2017

5. **Engelen, G., Rimmer, V., Joosen, W. (2021). Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study. IEEE SPW.**  
   Reference critique indispensable. Justifie audit, prudence et stress-tests.

6. **Rosay, A., Cheval, E., Carlier, F., Leroux, P. (2022). Network Intrusion Detection: A Comprehensive Analysis of CIC-IDS2017. ICISSP.**  
   Analyse detaillee des problemes de flows CICIDS2017 et proposition LycoSTand.

7. **Errors in the CICIDS2017 Dataset and the Significant Differences in Detection Performances It Makes (2023).**  
   Reference utile pour montrer que les erreurs de dataset changent les scores.

### B3. Evaluation pragmatique et deploiement

8. **Sommer, R., Paxson, V. (2010). Outside the Closed World: On Using Machine Learning for Network Intrusion Detection. IEEE S&P.**  
   Reference classique pour critiquer les evaluations ML trop fermees.

9. **Apruzzese, G., Laskov, P., Schneider, J. (2023). SoK: Pragmatic Assessment of Machine Learning for Network Intrusion Detection. IEEE EuroS&P.**  
   Reference centrale pour evaluation operationnelle du ML en NIDS.

10. **Apruzzese, G. (2026). SoK: Reshaping Research on Network Intrusion Detection Systems. ACM AsiaCCS.**  
    Reference recente pour renforcer le positionnement "repenser l'evaluation NIDS".

11. **Dietz et al. (2026). The Missing Link in Network Intrusion Detection: Taking AI/ML Research Efforts to Users.**  
    Utile pour justifier explicabilite, utilisabilite, reproductibilite, praticabilite.

### B4. Standardisation et generalisation

12. **Sarhan, M., Layeghy, S., Portmann, M. (2021). Towards a Standard Feature Set for Network Intrusion Detection System Datasets. Mobile Networks and Applications.**  
    Reference cle pour l'analogie avec FHIR/LOINC: standardiser les features pour ameliorer comparabilite et generalisation.

13. **Sarhan, M., Layeghy, S., Portmann, M. (2022). Evaluating Standard Feature Sets Towards Increased Generalisability and Explainability of ML-based Network Intrusion Detection. Big Data Research.**  
    Reference cle pour NetFlow vs CICFlowMeter et SHAP.

14. **Cantone, M., Marrocco, C., Bria, A. (2024). Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study. IEEE Access.**  
    Reference centrale pour montrer que generalisation cross-dataset est difficile.

### B5. Open-set, incertitude, calibration, XAI

15. **Unknown intrusion traffic detection method based on unsupervised learning / OpenMax (Scientific Reports, 2025).**  
    Reference recente pour open-set traffic detection.

16. **A Novel Open Set Energy-based Flow Classifier for Network Intrusion Detection.**  
    Utile pour unknown attack detection sur flows.

17. **Talpini et al. (2024). Enhancing trustworthiness in ML-based network intrusion detection with uncertainty quantification.**  
    Reference pour incertitude et predictions surconfiantes.

18. **Mohale, V. Z., Obagbuwa, I. C. (2025). Evaluating machine learning-based intrusion detection systems with explainable AI. Frontiers in Computer Science.**  
    Reference recente pour XAI en IDS.

### B6. Reproductibilite

19. **Reproducibility in Machine Learning-based Research: Overview, Barriers and Drivers (2024).**  
    Reference generale pour justifier data hash, feature hash, seeds, configs.

20. **MLflow documentation / Azure MLflow blog.**  
    Reference pratique pour experiment tracking.

---

## References web principales

- CICIDS2017 officiel: https://www.unb.ca/cic/datasets/ids-2017.html
- Papier original CICIDS2017: https://www.scitepress.org/papers/2018/66398/66398.pdf
- Troubleshooting CICIDS2017: https://intrusion-detection.distrinet-research.be/WTMC2021/Resources/wtmc2021_Engelen_Troubleshooting.pdf
- Survey datasets NIDS 2025: https://arxiv.org/abs/2502.06688
- Standard feature set NetFlow: https://arxiv.org/abs/2101.11315
- Generalisability + explainability: https://arxiv.org/abs/2104.07183
- Cross-dataset generalization: https://arxiv.org/abs/2402.10974
- Pragmatic ML for NIDS: https://arxiv.org/abs/2305.00550
- Reshaping NIDS research: https://arxiv.org/abs/2604.17556
- Open-set traffic detection: https://www.nature.com/articles/s41598-025-01084-1

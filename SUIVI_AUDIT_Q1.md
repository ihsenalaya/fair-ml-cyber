# Suivi Audit Q1 — FAIR-ML-CYBER

**Date audit initial** : 2026-06-17
**Dernier check** : 2026-06-17 (check #12)
**Auditeur** : Claude (Opus 4.8)
**Cible** : Publication Q1 (Computers & Security / IEEE TIFS / TDSC)
**Statut global** : 🟠 Quasi-prêt — 13/15 résolus. C3 seul critique restant (LR2000 s7/s99 en queue Azure). A5 mineur partiel.

---

## Légende

| Symbole | Signification |
|---|---|
| 🔴 | Critique — bloquant pour Q1 |
| 🟠 | Important — risque modéré de rejet |
| 🟡 | Mineur — amélioration recommandée |
| ✅ | Résolu |
| ⏳ | En cours / Partiel |
| ⬜ | À faire |

---

## PROBLÈMES CRITIQUES (bloquants)

### C1 — Second dataset complet manquant
- **Priorité** : 🔴 → ✅ RÉSOLU MINIMAL Q1
- **Statut** : ✅ CSE-CIC-IDS2018 **FULL sample** exécuté (363K flows, 10 CSV, 3 modèles). UNSW-NB15 bloqué côté accès officiel, documenté comme follow-up.
- **Vérification check #1** : 5 CSV, 200K flows partiel.
- **Vérification check #7** : **Upgrade majeur** — `evidence/cse-cic-ids2018-full-sample-s42-001/` présent avec :
  - 10 CSV publics, 16,232,943 lignes brutes, hash `96cd4ce8a085248a`
  - 363,648 lignes d'échantillon stratifié réel, hash `d3092e8e71a9680c`
  - 3 modèles (LR, HGB, RF), 4 splits, 0 warnings
  - Signal central reproduit : HGB CTS=0.1107 (random 0.9362 → temporal 0.1037)
  - UNSW-NB15 : accès bloqué par 403 SharePoint + erreur serveur CIC-UNSW. Documenté dans `UNSW_NB15_ACCESS_ATTEMPT.md` et `evidence/unsw-nb15-access-attempt-2026-06-17/`.
- **Problème restant** : Les 2 datasets sont du même écosystème CIC/UNB — réduit mais n'élimine pas les concerns d'external validity. Endpoint-pair impossible sur CSE-CIC (colonnes absentes/incomplètes). Seed 42 only pour l'externe.
- **Action restante non bloquante** : Obtenir UNSW/CIC-UNSW par accès légitime si possible; ne pas utiliser de miroir tiers sans l'étiqueter comme miroir. Ajouter seeds 7/99 externe si possible après C2/C3.
- **Impact** : Reviewer concern single-dataset fortement réduit. Signal CTS reproduit sur dataset externe gratuit, avec limite explicitée.

---

### C2 — Analyses avancées trois seeds
- **Priorité** : 🔴 → ✅ RÉSOLU
- **Statut** : ✅ s42 + s7 + s99 tous présents avec artefacts complets
- **Vérification check #10** : `evidence/advanced-core-s7-001/` apparu avec 12 fichiers :
  - binary_results, multiclass_results, per_class_results, rare_class_results
  - open_set_results, calibration_bins, abstention_curves
  - feature_importance, explanation_stability, events.jsonl, summary.json, audit_summary.json
  - Seed : 7 | Hash données : `f51899df9bd60758` (cohérent) | 10 binary + 10 multiclass + 8 open-set runs
- **Résultats s7 confirmés cohérents cross-seed** :
  - HGB binary : random 0.9960 → temporal 0.2300 (s42: 0.2296, s99: 0.2297) ✅
  - LR binary : random 0.9345 → temporal 0.5395 (s42: 0.5395, s99: 0.5395) ✅
  - XAI Jaccard HGB temporal s7 : **0.20** (s42: 0.07, s99: 0.11) — instabilité HGB confirmée 3 seeds ✅
  - XAI Jaccard LR temporal s7 : **0.5789** (s42: 0.5789, s99: 0.7647) — stabilité LR confirmée 3 seeds ✅

---

### C3 — Convergence LR non résolue sur seeds 7 & 99
- **Priorité** : 🔴 CRITIQUE
- **Statut** : ⏳ Jobs en queue Azure ML — aucun artefact encore
- **Vérification check #1** : fullcore-lr2000-s42-001 terminé.
- **Vérification check #7** : `ADVANCED_CORE_MULTI_SEED_STATUS.md` Azure Queue Status confirme : `fullcore-lr2000-nohour-s42-001`, `fullcore-lr2000-nohour-s7-001`, `fullcore-lr2000-nohour-s99-001` tous en statut **Queued**. Aucun artefact dans `evidence/`.
- **Problème restant** : Tables LR multi-seed utilisent encore max_iter=500 pour s7/s99.
- **Action restante** : Attendre fin des jobs Queued. Télécharger artefacts. Mettre à jour FULLCORE_MEM_MULTI_SEED_RESULTS.md.
- **Effort estimé** : ~80 min compute (jobs en queue)

---

### C4 — Discussion, Conclusion et Threats manquantes
- **Priorité** : 🔴 → ✅ RÉSOLU
- **Statut** : ✅ Complet
- **Vérification check #1** : `paper/main.tex` contient :
  - `\section{Discussion}` ligne 346 — contenu substantiel (3–5 §)
  - `\section{Threats to Validity}` ligne 356 — contenu substantiel
  - `\section{Conclusion}` ligne 376 — contenu substantiel
- **Note** : Le fichier SUIVI initial était erroné. Ces sections existaient déjà.

---

## PROBLÈMES IMPORTANTS (risque modéré)

### I1 — Calibration mesurée mais non corrigée
- **Priorité** : 🟠 → ✅ RÉSOLU
- **Statut** : ✅ Complet
- **Vérification check #1** : `src/fair_ml_cyber/calibration.py` contient `_platt_calibrate()` et `_isotonic_calibrate()` (IsotonicRegression sklearn). Résultats dans CSE_CIC_IDS2018_PARTIAL_RESULTS.md : isotonic réduit ECE LR de 0.3619 → 0.1533 (temporel). Implémentation et résultats présents.

---

### I2 — Open-set trop basique
- **Priorité** : 🟠 → ✅ RÉSOLU
- **Statut** : ✅ Complet
- **Vérification check #1** : `src/fair_ml_cyber/open_set.py` ligne 25 : `DEFAULT_OPEN_SET_MODELS = ["isolation_forest", "local_outlier_factor"]`. Fonction `run_open_set_baselines()` (ligne 48) gère les deux. Résultats CSE-CIC : LOF AUROC 0.8990/0.9574/0.9087 pour Web/Botnet/BruteForce unknown.

---

### I3 — Related Work insuffisant
- **Priorité** : 🟠 → ✅ RÉSOLU
- **Statut** : ✅ Résolu
- **Vérification check #1** : `paper/main.tex` contient 4 subsections Related Work. `references.bib` : 18 entrées totales. Insuffisant pour Q1.
- **Vérification check #3** : 11 citations uniques dans Related Work, 18 entrées .bib.
- **Vérification check #4** : **33 entrées BibTeX** dans `references.bib` (+15 depuis check #3), 12 `\cite{}` uniques dans Related Work référençant 14+ entrées. Expansion substantielle — seuil Q1 atteint.

---

### I4 — Stabilité XAI sous-développée
- **Priorité** : 🟠 → ✅ RÉSOLU AU NIVEAU MANUSCRIT
- **Statut** : ✅ Limitation reconnue et encadrée dans `paper/main.tex`
- **Vérification check #8** : `paper/main.tex` reconnaît explicitement la limitation à deux endroits :
  - Ligne 353 : *"current HGB permutation importance uses a sample size of 2000 and one repeat; a final journal version should increase repeats and add uncertainty estimates."*
  - Ligne 410 : *"HGB explanation stability uses lightweight permutation importance. A final version should use more repeats and confidence intervals."*
- Résultats cross-seed disponibles (s42 + s99) montrant la même tendance Jaccard instable pour HGB.
- **Note** : La limitation expérimentale est documentée honnêtement — approche académique acceptable pour soumission initiale. Les reviewers peuvent demander un rerun mais le papier ne cache pas la faiblesse.

---

### I5 — Endpoint-pair holdout non discriminant
- **Priorité** : 🟠 → ✅ RÉSOLU
- **Statut** : ✅ Discuté dans le manuscrit
- **Vérification check #1** : `paper/main.tex` section Discussion (ligne 346) mentionne : *"Endpoint-pair holdout remains high for both models and should not be over-interpreted as proof of deployment robustness."* Limite encadrée explicitement.

---

## AMÉLIORATIONS RECOMMANDÉES (mineur)

### A1 — Justification formelle de la métrique CTS
- **Priorité** : 🟡 MINEUR
- **Statut** : ✅ Résolu
- **Vérification check #2** : Section CTS de `paper/main.tex` étendue : CTS est présenté comme ratio de robustesse relatif, non substitut de macro-F1 absolu, utile pour comparer la part de performance random qui survit sous shift.
- **Vérification check #3** : CONFIRMÉ — lignes 161–168 de main.tex, 7 lignes de justification avec comparaison explicite à macro-F1 absolu.

---

### A2 — Figure heatmap classe × split protocol
- **Priorité** : 🟡 MINEUR
- **Statut** : ✅ Résolu
- **Vérification check #2** : `paper/figures/per_class_f1_heatmap_hgb.png` générée depuis `advanced_core_s42_per_class_results.csv` et intégrée dans `paper/main.tex`. Les cellules grises indiquent les classes absentes du test split.
- **Vérification check #3** : CONFIRMÉ — fichier 134 KB présent, `\includegraphics` ligne 295 de main.tex, label `fig:per-class-heatmap`.

---

### A3 — Tableau décisionnel praticien (SOC)
- **Priorité** : 🟡 MINEUR
- **Statut** : ✅ Résolu
- **Vérification check #2** : Tableau `Practical SOC guidance` ajouté dans `paper/main.tex`, couvrant choix de modèle, validation temporelle/scénario, calibration/abstention, rare attacks et reporting opérationnel.
- **Vérification check #3** : CONFIRMÉ — `\subsection{Practical SOC guidance}` lignes 355–378, Table~\ref{tab:soc-guidance} avec 5 dimensions couvertes.

---

### A4 — Justifier le choix des 3 modèles
- **Priorité** : 🟡 MINEUR
- **Statut** : ✅ Résolu
- **Vérification check #2** : Section Models mise à jour : LR/HGB comme baselines tabulaires reproductibles, RF validé en pilote/externe mais non full-data pour risque mémoire/artefacts, pas de DNN car le papier n'est pas un claim SOTA.
- **Vérification check #3** : CONFIRMÉ — ligne 113 de main.tex : *"We do not claim a new detector architecture and therefore do not optimize deep neural networks in this manuscript."*

---

### A5 — Artifacts publics + DOI Zenodo
- **Priorité** : 🟡 MINEUR
- **Statut** : ⏳ Partiel — GitHub Release créée; release courante `v1.0.1` prévue pour inclure seed 7, DOI Zenodo absent; manuscrit mentionne explicitement le DOI pending
- **Vérification check #1** : `.git/refs/tags/` vide.
- **Vérification check #9** : tag annoté `v1.0.0` poussé et pointant vers `5ccb965925089bca44e3073cd7b5168121106cb4`; GitHub Release publiée : https://github.com/ihsenalaya/fair-ml-cyber/releases/tag/v1.0.0 avec `FAIR-ML-CYBER-main.pdf` comme asset.
- **Blocage Zenodo** : aucun token `ZENODO_ACCESS_TOKEN`/`ZENODO_TOKEN` local; recherche Zenodo sans dépôt correspondant. DOI non généré automatiquement.
- **Vérification check #12** : `paper/main.tex` cite la GitHub Release courante `v1.0.1` et indique que le DOI Zenodo n'est pas encore émis.
- **Action restante** : connecter le repo GitHub à Zenodo ou fournir un token Zenodo; publier le DOI puis remplacer la mention pending dans `paper/main.tex` par le DOI final.

---

### A6 — Effect sizes dans les tables principales
- **Priorité** : 🟡 MINEUR
- **Statut** : ⏳ Délibérément omis — documenté
- **Vérification check #1** : `paper/main.tex` ligne 191 : *"Standardized effect sizes are not shown in the table because very low inter-seed variance can make them numerically unstable."* Choix volontaire et justifié. Tables contiennent deltaF1 et ratios.
- **Action** : Aucune — choix documenté acceptable.

---

## ÉTAT DU MANUSCRIT

| Section | État | Priorité |
|---|---|---|
| Abstract | ✅ Complet | — |
| Introduction | ✅ Complet | — |
| Related Work | ✅ Renforcé (33 entrées BibTeX) | — |
| Dataset & Audit | ✅ Complet | — |
| Methods | ✅ Complet | — |
| Results | ✅ Tables + figures + validation externe CSE-CIC full-sample | — |
| Discussion | ✅ Présente et renforcée (check #2) | — |
| Threats to Validity | ✅ Présente et formalisée (check #2) | — |
| Conclusion | ✅ Présente (vérifié check #1) | — |
| Practical Guidance (tableau SOC) | ✅ Présente (check #2) | — |

---

## TABLEAU RÉCAPITULATIF DES STATUTS

| Point | Priorité | Statut | Résolu check #1 |
|---|---|---|---|
| C1 — Second dataset | 🔴 | ✅ Résolu minimal Q1 | **OUI** (check #7) |
| C2 — Advanced seeds 7&99 | 🔴 | ✅ Résolu | **OUI** (check #10) |
| C3 — LR convergence s7/s99 | 🔴 | ⏳ Jobs en queue | Non |
| C4 — Discussion/Conclusion | 🔴 | ✅ Résolu | **OUI** |
| I1 — Calibration post-hoc | 🟠 | ✅ Résolu | **OUI** |
| I2 — Open-set baselines | 🟠 | ✅ Résolu | **OUI** |
| I3 — Related Work | 🟠 | ✅ Résolu | **OUI** (check #4) |
| I4 — XAI stabilité | 🟠 | ✅ Résolu (limitation documentée manuscrit) | **OUI** (check #8) |
| I5 — Endpoint-pair | 🟠 | ✅ Résolu | **OUI** |
| A1 — CTS justification | 🟡 | ✅ Résolu | **OUI** |
| A2 — Heatmap | 🟡 | ✅ Résolu | **OUI** |
| A3 — Tableau SOC | 🟡 | ✅ Résolu | **OUI** |
| A4 — Choix modèles | 🟡 | ✅ Résolu | **OUI** |
| A5 — DOI Zenodo | 🟡 | ⏳ Release GitHub faite, release courante v1.0.1, DOI pending mentionné, DOI final manquant | Non |
| A6 — Effect sizes | 🟡 | ⏳ Délibéré | **OUI** |

**Résolus** : C1, C2, C4, I1, I2, I3, I4, I5, A1, A2, A3, A4, A6 = **13 points fermés**
**Bloquant restant** : C3 (1 critique — dépend Azure ML)
**Partiels mineurs** : A5 (release GitHub faite, DOI Zenodo absent, mention pending dans le manuscrit)

---

## ROADMAP MISE À JOUR

### Urgences immédiates (dès que jobs Azure terminés)
- [x] **C2** : Télécharger artefacts advanced-core-s7 → compléter tables avancées 3 seeds
- [ ] **C3** : Télécharger artefacts fullcore-lr2000-nohour-s7 & s99 → mettre à jour tables LR multi-seed

### Court terme (1–2 semaines)
- [x] **C1** : Validation externe CSE-CIC-IDS2018 full-sample exécutée et intégrée
- [ ] **C1 follow-up** : Obtenir UNSW/CIC-UNSW par accès officiel légitime si disponible
- [x] **I3** : Ajouter ~10 références dans Related Work (distribution shift, benchmark validity post-2023)
- [ ] **I4** : Augmenter permutation repeats à ≥5 + CI bootstrap sur importances

### Finalisation (semaine 3–4)
- [x] **A1** : Étendre justification CTS avec comparaison vs robustesse relative
- [x] **A2** : Créer heatmap F1 per-class × split protocol
- [x] **A3** : Ajouter tableau Practical Guidance (SOC)
- [x] **A4** : 1–2 phrases justifiant absence DNN
- [~] **A5** : Release GitHub faite (`v1.0.1` pour l'état courant), DOI pending mentionné dans le manuscrit, DOI Zenodo final à générer
- [ ] Révision interne complète + soumission

---

## ÉVALUATION DE VIABILITÉ Q1

| Journal | Probabilité actuelle | Après C3 résolu |
|---|---|---|
| Computers & Security (Q1, Elsevier) | ~60–65% | ~70% |
| Expert Systems with Applications (Q1) | ~40% | ~50% |
| IEEE TIFS (Q1) | ~25% | ~40% |
| IEEE TDSC (Q1) | ~10–15% | ~20% (sauf ajout algo) |

---

## FORCES DU PAPIER (à ne pas diluer)

1. Angle original : étude de validité des benchmarks, pas un nouveau modèle
2. Signal fort et reproductible : HGB 0.9977 → 0.2315 (temporel), vérifié 3 seeds
3. Infrastructure reproductible : hashes, seeds, Azure ML provenance, 28 tests passants
4. Évaluation multi-facettes : binaire, multiclasse, rare-class, open-set, calibration, XAI
5. Honnêteté scientifique : aucun faux claim SOTA, framing explicite benchmark study

> **Message central à conserver** : *"Les benchmarks NIDS surestiment massivement la robustesse réelle. Notre framework stress-test reproductible quantifie ce gap de manière rigoureuse."*

---

## HISTORIQUE DES CHECKS

| Check | Date | Points résolus | Points ouverts |
|---|---|---|---|
| Initial | 2026-06-17 | 0 | 15 |
| Check #1 | 2026-06-17 | 5 (C4, I1, I2, I5, A6) | 10 |
| Check #2 | 2026-06-17 | +4 (A1, A2, A3, A4) — 9 total | 6 |
| Check #3 | 2026-06-17 | 0 nouveaux — confirmations A1–A4 ✅, C1/C2/C3 toujours bloquants | 6 |
| Check #4 | 2026-06-17 | +1 (I3 ✅ — references.bib 18→33 entrées) — 10 total | 5 |
| Check #5 | 2026-06-17 | 0 nouveau — C1/C2/C3 toujours bloquants Azure/données, I4/A5 inchangés | 5 |
| Check #6 | 2026-06-17 | C2 avance : advanced-core-s99-001 arrivé. s7 toujours manquant. 10/15 résolus | 5 |
| Check #7 | 2026-06-17 | +1 (C1 ✅ via CSE-CIC full-sample 10 CSV/363K rows + UNSW access documenté) — 11 total | 4 |
| Check #8 | 2026-06-17 | +1 (I4 ✅ — limitation XAI documentée dans main.tex lignes 353/410) — 12 total | 3 |
| Check #9 | 2026-06-17 | A5 avance : tag v1.0.0 créé. C2/C3 toujours en attente Azure ML. 12/15 résolus | 3 |
| Check #10 | 2026-06-17 | **C2 ✅** — advanced-core-s7-001 arrivé, 3 seeds confirmés cohérents. 13/15 résolus | 2 |
| Check #11 | 2026-06-17 | 0 nouveau — C3 toujours en queue Azure, A5 DOI toujours absent. 13/15 résolus | 2 |
| Check #12 | 2026-06-17 | 0 nouveau résolu — A5 clarifié dans `paper/main.tex` avec release courante `v1.0.1` et DOI Zenodo pending. C3 toujours en queue. 13/15 résolus | 2 |

---

*Mis à jour automatiquement à chaque check — prochain check dans ~20 min.*

# Audit des Donnees

## Source locale

Chemin inspecté:

`/mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs`

## Nature des données

Les fichiers contiennent des **flux réseau labellisés** pour la détection d'intrusion. Les colonnes ne sont pas cliniques; elles décrivent des caractéristiques de trafic:

- identifiants et endpoints: `flow_id`, `src_ip`, `src_port`, `dst_ip`, `dst_port`;
- protocole et durée: `protocol`, `duration`;
- volumes et paquets: `packets_count`, `fwd_packets_count`, `bwd_packets_count`, `total_payload_bytes`;
- statistiques de payload: max, min, mean, std, variance;
- flags TCP: `fin_flag_counts`, `syn_flag_counts`, `ack_flag_counts`, etc.;
- inter-arrival time: `packet_IAT_*`, `fwd_packets_IAT_*`, `bwd_packets_IAT_*`;
- label final: `label`.

Chaque fichier a le même schéma: **122 colonnes**.

## Taille et distribution

Total: **2 438 052 flux** dans **18 fichiers CSV**.

| Label | Lignes | Pourcentage |
|---|---:|---:|
| Benign | 1 786 239 | 73.2650% |
| DoS_Hulk | 349 240 | 14.3246% |
| Port_Scan | 161 323 | 6.6169% |
| DDoS_LOIT | 95 733 | 3.9266% |
| FTP-Patator | 9 531 | 0.3909% |
| DoS_GoldenEye | 8 364 | 0.3431% |
| DoS_Slowhttptest | 6 860 | 0.2814% |
| SSH-Patator | 5 949 | 0.2440% |
| Botnet_ARES | 5 508 | 0.2259% |
| DoS_Slowloris | 5 177 | 0.2123% |
| Web_Brute_Force | 2 734 | 0.1121% |
| Web_XSS | 1 358 | 0.0557% |
| Web_SQL_Injection | 24 | 0.0010% |
| Heartbleed | 12 | 0.0005% |

## Fichiers

| Fichier | Lignes | Label principal | Fenêtre temporelle |
|---|---:|---|---|
| `monday_benign.csv` | 495 338 | Benign | 2017-07-03 |
| `tuesday_benign.csv` | 395 976 | Benign | 2017-07-04 |
| `wednesday_benign.csv` | 397 053 | Benign | 2017-07-05 |
| `thursday_benign.csv` | 133 770 | Benign | 2017-07-06 |
| `friday_benign.csv` | 364 102 | Benign | 2017-07-07 |
| `ftp_patator.csv` | 9 531 | FTP-Patator | 2017-07-04 |
| `ssh_patator-new.csv` | 5 949 | SSH-Patator | 2017-07-04 |
| `dos_slowloris.csv` | 5 177 | DoS_Slowloris | 2017-07-05 |
| `dos_slowhttptest.csv` | 6 860 | DoS_Slowhttptest | 2017-07-05 |
| `dos_hulk.csv` | 349 240 | DoS_Hulk | 2017-07-05 |
| `dos_golden_eye.csv` | 8 364 | DoS_GoldenEye | 2017-07-05 |
| `heartbleed.csv` | 12 | Heartbleed | 2017-07-05 |
| `web_brute_force.csv` | 2 734 | Web_Brute_Force | 2017-07-06 |
| `web_xss.csv` | 1 358 | Web_XSS | 2017-07-06 |
| `web_sql_injection.csv` | 24 | Web_SQL_Injection | 2017-07-06 |
| `portscan.csv` | 161 323 | Port_Scan | 2017-07-07 |
| `botnet_ares.csv` | 5 508 | Botnet_ARES | 2017-07-07 |
| `ddos_loit.csv` | 95 733 | DDoS_LOIT | 2017-07-07 |

## Adequation pour un article cyber

Ces données sont **adaptées** à un article sur:

- détection d'intrusion réseau flow-based;
- classification binaire benign/attack;
- classification multi-classe par famille d'attaque;
- problème de classes rares;
- evaluation réaliste de modèles NIDS;
- robustesse contre les fuites expérimentales;
- explicabilité et coût de déploiement.

Ces données sont **insuffisantes** pour:

- inspection payload/deep packet inspection, car seuls les flux agrégés sont disponibles;
- correction fine des labels depuis les PCAP, car les PCAP originaux ne sont pas dans ce dossier;
- revendication forte de généralisation à des réseaux modernes sans validation externe;
- détection d'attaques zero-day au sens strict, sauf protocole open-set simulé par holdout d'une famille d'attaque.

## Risques scientifiques du dataset

1. **Dataset ancien**: scénarios 2017.
2. **Simulation contrôlée**: pas un réseau de production réel.
3. **Déséquilibre extrême**: Heartbleed et SQL Injection ont respectivement 12 et 24 flux.
4. **Risque de fuite par contexte**: timestamps, IPs, ports et scénarios journaliers peuvent faciliter une classification non généralisable.
5. **Labels probablement hérités de CICIDS2017**: la littérature a documenté des erreurs de labellisation et des artefacts dans CICIDS2017.

## Verdict

Les données sont utilisables pour un article Q1 **si** l'article ne vend pas simplement une accuracy élevée. Le bon angle est:

> transformer ces CSV en banc d'essai reproductible pour mesurer la robustesse réelle des NIDS sous protocoles temporels, open-set, anti-fuite, calibrés et explicables.

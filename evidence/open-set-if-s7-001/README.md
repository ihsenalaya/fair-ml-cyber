# open-set-if-s7-001 Evidence Snapshot

Azure ML Isolation Forest open-set baseline for seed 7.

| Item | Value |
|---|---|
| Azure ML job | `open-set-if-s7-001` |
| Seed | 7 |
| Model | `isolation_forest` |
| Feature tier | `deployment_safe` |
| Unknown families | `Web`, `Botnet`, `PortScan`, `DDoS` |
| Rows | 2,438,052 |
| Completed / failed | 4 / 0 |
| Warning sum | 0 |
| Convergence warning sum | 0 |

## Files

- `audit_summary.json`
- `open_set_if_s7_results.csv`
- `open_set_if_s7_summary.json`
- `open_set_if_s7_events.jsonl`

## Key Results

| Unknown family | AUROC | AUPRC | Unknown support |
|---|---:|---:|---:|
| `Web` | 0.714252 | 0.020379 | 4,116 |
| `Botnet` | 0.763453 | 0.042076 | 5,508 |
| `PortScan` | 0.891664 | 0.643767 | 161,323 |
| `DDoS` | 0.966344 | 0.731857 | 95,733 |

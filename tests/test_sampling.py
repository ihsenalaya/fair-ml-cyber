import pandas as pd

from fair_ml_cyber.sampling import build_stratified_sample


def test_build_stratified_sample_caps_large_labels_and_keeps_rare(tmp_path):
    csv_dir = tmp_path / "raw"
    csv_dir.mkdir()
    rows = []
    for i in range(20):
        rows.append(
            {
                "Timestamp": f"14/02/2018 08:31:{i:02d}",
                "Dst Port": 80,
                "Protocol": 6,
                "Flow Duration": i + 1,
                "Label": "Benign",
            }
        )
    for i in range(10):
        rows.append(
            {
                "Timestamp": f"14/02/2018 08:32:{i:02d}",
                "Dst Port": 22,
                "Protocol": 6,
                "Flow Duration": i + 1,
                "Label": "SSH-Bruteforce",
            }
        )
    rows.append(
        {
            "Timestamp": "14/02/2018 08:33:00",
            "Dst Port": 80,
            "Protocol": 6,
            "Flow Duration": 1,
            "Label": "Brute Force -Web",
        }
    )
    pd.DataFrame(rows).to_csv(csv_dir / "raw.csv", index=False)

    summary = build_stratified_sample(
        csv_dir,
        tmp_path / "sample",
        benign_cap=5,
        attack_cap=6,
        seed=1,
    )

    sample = pd.read_csv(summary["output_path"])
    counts = sample["label"].value_counts().to_dict()
    assert counts["Benign"] == 5
    assert counts["SSH-Bruteforce"] == 6
    assert counts["Brute Force -Web"] == 1

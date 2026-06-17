import pandas as pd

from fair_ml_cyber.audit import audit_csv_dir
from fair_ml_cyber.data import load_csvs, prepare_dataframe
from fair_ml_cyber.features import select_feature_tier


def test_prepare_dataframe_accepts_cse_cic_ids2018_headers():
    df = prepare_dataframe(
        pd.DataFrame(
            {
                "Dst Port": [80, 22, 443],
                "Protocol": [6, 6, 6],
                "Timestamp": [
                    "14/02/2018 08:31:01",
                    "22/02/2018 09:01:02",
                    "02/03/2018 10:11:12",
                ],
                "Flow Duration": [1, 2, 3],
                "Flow Byts/s": [10.0, 20.0, 30.0],
                "Label": ["Benign", "FTP-BruteForce", "Brute Force -Web"],
            }
        )
    )

    assert "dst_port" in df.columns
    assert "flow_byts_per_s" in df.columns
    assert df["binary_label"].tolist() == [0, 1, 1]
    assert df["attack_family"].tolist() == ["Benign", "BruteForce", "Web"]
    assert df["day"].tolist() == ["2018-02-14", "2018-02-22", "2018-03-02"]

    tier = select_feature_tier(df, "deployment_safe")
    assert "dst_port" not in tier.columns
    assert "hour" not in tier.columns
    assert "flow_duration" in tier.columns


def test_audit_accepts_canonicalized_label_header(tmp_path):
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    pd.DataFrame(
        {
            "Dst Port": [80, 22],
            "Protocol": [6, 6],
            "Timestamp": ["14/02/2018 08:31:01", "14/02/2018 08:32:01"],
            "Flow Duration": [1, 2],
            "Label": ["Benign", "SSH-Bruteforce"],
        }
    ).to_csv(csv_dir / "cse.csv", index=False)

    audit = audit_csv_dir(csv_dir, tmp_path / "audit")

    assert audit["total_rows"] == 2
    assert audit["columns"][-1] == "label"
    assert audit["labels"][0]["label"] == "Benign"


def test_load_csvs_samples_without_keeping_repeated_header_rows(tmp_path):
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    pd.DataFrame(
        {
            "Dst Port": [80, "Dst Port", 22, 443],
            "Protocol": [6, "Protocol", 6, 6],
            "Timestamp": [
                "14/02/2018 08:31:01",
                "Timestamp",
                "14/02/2018 08:32:01",
                "14/02/2018 08:33:01",
            ],
            "Flow Duration": [1, "Flow Duration", 2, 3],
            "Label": ["Benign", "Label", "SSH-Bruteforce", "Benign"],
        }
    ).to_csv(csv_dir / "cse.csv", index=False)

    df = load_csvs(csv_dir, sample_per_file=10, random_state=1)

    assert df["label"].tolist().count("Label") == 0
    assert len(df) == 3

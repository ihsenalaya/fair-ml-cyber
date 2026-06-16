import pandas as pd

from fair_ml_cyber.features import make_xy, select_feature_tier


def _df():
    return pd.DataFrame(
        {
            "flow_id": ["a", "b"],
            "timestamp": ["2020-01-01", "2020-01-02"],
            "src_ip": ["1.1.1.1", "1.1.1.2"],
            "dst_ip": ["2.2.2.2", "2.2.2.3"],
            "src_port": [10, 11],
            "dst_port": [80, 443],
            "protocol": [6, 6],
            "duration": [1.0, 2.0],
            "packets_count": [3, 4],
            "payload_bytes_mean": [10.0, 12.0],
            "label": ["Benign", "DoS_Hulk"],
            "binary_label": [0, 1],
            "attack_family": ["Benign", "DoS"],
        }
    )


def test_deployment_safe_excludes_ports_and_identity():
    tier = select_feature_tier(_df(), "deployment_safe")
    assert "src_port" not in tier.columns
    assert "dst_port" not in tier.columns
    assert "duration" in tier.columns


def test_feature_tier_excludes_all_missing_numeric_columns():
    df = _df()
    df["protocol"] = pd.NA
    tier = select_feature_tier(df, "no_identity")
    assert "protocol" not in tier.columns


def test_make_xy_returns_target():
    X, y, tier = make_xy(_df(), "no_identity", target="binary_label")
    assert len(X) == 2
    assert y.tolist() == [0, 1]
    assert tier.name == "no_identity"

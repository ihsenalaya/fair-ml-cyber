import pandas as pd

from fair_ml_cyber.data import prepare_dataframe
from fair_ml_cyber.splits import random_split, temporal_split


def _df():
    rows = []
    for i in range(20):
        rows.append(
            {
                "flow_id": f"f{i}",
                "timestamp": f"2017-07-0{1 + (i // 10)} 00:00:{i:02d}",
                "src_ip": f"10.0.0.{i}",
                "src_port": 1000 + i,
                "dst_ip": "10.0.1.1",
                "dst_port": 80,
                "protocol": 6,
                "duration": float(i + 1),
                "packets_count": i + 2,
                "label": "Benign" if i % 2 == 0 else "DoS_Hulk",
            }
        )
    return prepare_dataframe(pd.DataFrame(rows))


def test_random_split_covers_rows():
    df = _df()
    split = random_split(df, target="label", seed=7)
    all_idx = set(split.train_idx) | set(split.val_idx) | set(split.test_idx)
    assert all_idx == set(df.index)
    assert set(split.train_idx).isdisjoint(split.test_idx)


def test_random_split_records_when_rare_class_prevents_stratification():
    df = _df()
    df.loc[0, "label"] = "Heartbleed"
    df = prepare_dataframe(df)

    split = random_split(df, target="label", seed=7)

    all_idx = set(split.train_idx) | set(split.val_idx) | set(split.test_idx)
    assert all_idx == set(df.index)
    assert split.metadata["train_stratified"] is False
    assert split.metadata["train_pool_class_summary"]["min_class_count"] == 1


def test_temporal_split_ordered():
    df = _df()
    split = temporal_split(df)
    assert max(split.train_idx) < min(split.test_idx)

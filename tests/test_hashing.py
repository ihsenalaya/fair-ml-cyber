import pandas as pd

from fair_ml_cyber.hashing import hash_dataframe, hash_object


def test_hash_dataframe_stable():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    assert hash_dataframe(df) == hash_dataframe(df.copy())


def test_hash_object_order_independent():
    assert hash_object({"a": 1, "b": 2}) == hash_object({"b": 2, "a": 1})


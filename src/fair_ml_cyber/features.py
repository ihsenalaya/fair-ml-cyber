"""Feature tier selection."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


IDENTITY_COLUMNS = {
    "flow_id",
    "timestamp",
    "timestamp_dt",
    "src_ip",
    "dst_ip",
    "source_file",
    "day",
    "hour",
}
TARGET_COLUMNS = {"label", "binary_label", "attack_family"}
PORT_COLUMNS = {"src_port", "dst_port"}


@dataclass(frozen=True)
class FeatureTier:
    name: str
    columns: list[str]
    excluded_columns: list[str]


def numeric_columns(df: pd.DataFrame) -> list[str]:
    return [
        c
        for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c]) and c not in TARGET_COLUMNS and df[c].notna().any()
    ]


def select_feature_tier(df: pd.DataFrame, tier: str) -> FeatureTier:
    nums = numeric_columns(df)
    excluded: set[str] = set()

    if tier == "full_leaky":
        cols = nums
    elif tier == "no_identity":
        excluded = IDENTITY_COLUMNS
        cols = [c for c in nums if c not in excluded]
    elif tier == "flow_basic":
        keep_terms = [
            "protocol",
            "duration",
            "packets_count",
            "payload_bytes",
            "bytes_rate",
            "packets_rate",
            "down_up_rate",
        ]
        excluded = IDENTITY_COLUMNS
        cols = [c for c in nums if c not in excluded and any(term in c for term in keep_terms)]
    elif tier == "flow_statistical":
        keep_terms = [
            "payload",
            "header",
            "iat",
            "IAT",
            "flag",
            "subflow",
            "segment",
            "bulk",
            "active",
            "idle",
        ]
        excluded = IDENTITY_COLUMNS
        cols = [c for c in nums if c not in excluded and any(term in c for term in keep_terms)]
    elif tier == "deployment_safe":
        excluded = IDENTITY_COLUMNS | PORT_COLUMNS
        cols = [c for c in nums if c not in excluded]
    else:
        raise ValueError(f"Unknown feature tier: {tier}")

    return FeatureTier(name=tier, columns=cols, excluded_columns=sorted(excluded))


def make_xy(
    df: pd.DataFrame,
    tier: str,
    target: str = "binary_label",
) -> tuple[pd.DataFrame, pd.Series, FeatureTier]:
    ft = select_feature_tier(df, tier)
    X = df[ft.columns].copy()
    y = df[target].copy()
    X = X.replace([float("inf"), float("-inf")], pd.NA)
    return X, y, ft

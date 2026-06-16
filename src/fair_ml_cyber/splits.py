"""Experimental split protocols."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from fair_ml_cyber.hashing import hash_object


@dataclass(frozen=True)
class SplitIndices:
    name: str
    train_idx: list[int]
    val_idx: list[int]
    test_idx: list[int]
    metadata: dict

    @property
    def split_hash(self) -> str:
        return hash_object(
            {
                "name": self.name,
                "train": self.train_idx,
                "val": self.val_idx,
                "test": self.test_idx,
                "metadata": self.metadata,
            }
        )


def _class_count_summary(values: pd.Series) -> dict:
    counts = values.astype(str).value_counts(dropna=False)
    return {
        "num_classes": int(counts.shape[0]),
        "min_class_count": int(counts.min()) if not counts.empty else 0,
        "max_class_count": int(counts.max()) if not counts.empty else 0,
    }


def _can_stratify(values: pd.Series, n_samples: int) -> bool:
    counts = values.astype(str).value_counts(dropna=False)
    if counts.shape[0] < 2:
        return False
    if int(counts.min()) < 2:
        return False
    if n_samples <= counts.shape[0]:
        return False
    return True


def _safe_train_test_split(
    idx,
    target_values: pd.Series,
    *,
    train_size: float,
    seed: int,
) -> tuple:
    stratify = target_values.astype(str) if _can_stratify(target_values, len(idx)) else None
    train_idx, test_idx = train_test_split(
        idx,
        train_size=train_size,
        random_state=seed,
        stratify=stratify,
    )
    return train_idx, test_idx, stratify is not None, _class_count_summary(target_values)


def random_split(df: pd.DataFrame, target: str = "label", seed: int = 42) -> SplitIndices:
    idx = df.index.to_numpy()
    train_idx, tmp_idx, train_stratified, train_counts = _safe_train_test_split(
        idx,
        df[target],
        train_size=0.70,
        seed=seed,
    )
    val_idx, test_idx, val_test_stratified, val_test_counts = _safe_train_test_split(
        tmp_idx,
        df.loc[tmp_idx, target],
        train_size=0.50,
        seed=seed,
    )
    return SplitIndices(
        "random_stratified",
        train_idx.tolist(),
        val_idx.tolist(),
        test_idx.tolist(),
        {
            "seed": seed,
            "target": target,
            "train_stratified": train_stratified,
            "val_test_stratified": val_test_stratified,
            "train_pool_class_summary": train_counts,
            "val_test_pool_class_summary": val_test_counts,
        },
    )


def temporal_split(df: pd.DataFrame) -> SplitIndices:
    if "timestamp_dt" not in df.columns:
        raise ValueError("timestamp_dt is required for temporal split")
    ordered = df.sort_values("timestamp_dt", kind="mergesort").index.to_list()
    n = len(ordered)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)
    return SplitIndices(
        "temporal",
        ordered[:train_end],
        ordered[train_end:val_end],
        ordered[val_end:],
        {"train_frac": 0.70, "val_frac": 0.15},
    )


def day_holdout_split(df: pd.DataFrame, holdout_day: str, seed: int = 42) -> SplitIndices:
    test_idx = df.index[df["day"].astype(str) == str(holdout_day)].to_numpy()
    rest_idx = df.index[df["day"].astype(str) != str(holdout_day)].to_numpy()
    train_idx, val_idx, stratified, class_summary = _safe_train_test_split(
        rest_idx,
        df.loc[rest_idx, "label"],
        train_size=0.82,
        seed=seed,
    )
    return SplitIndices(
        f"day_holdout_{holdout_day}",
        train_idx.tolist(),
        val_idx.tolist(),
        test_idx.tolist(),
        {
            "holdout_day": holdout_day,
            "seed": seed,
            "train_val_stratified": stratified,
            "train_val_pool_class_summary": class_summary,
        },
    )


def scenario_holdout_split(df: pd.DataFrame, holdout_family: str, seed: int = 42) -> SplitIndices:
    holdout_mask = df["attack_family"].astype(str) == holdout_family
    benign_mask = df["attack_family"].astype(str) == "Benign"
    test_attack_idx = df.index[holdout_mask].to_numpy()
    benign_idx = df.index[benign_mask].to_numpy()
    if len(test_attack_idx) == 0:
        raise ValueError(f"No rows for holdout family {holdout_family}")
    benign_test, benign_rest = train_test_split(benign_idx, test_size=0.80, random_state=seed)
    train_pool = df.index[~holdout_mask & ~df.index.isin(benign_test)].to_numpy()
    train_idx, val_idx, stratified, class_summary = _safe_train_test_split(
        train_pool,
        df.loc[train_pool, "label"],
        train_size=0.82,
        seed=seed,
    )
    test_idx = list(test_attack_idx) + list(benign_test)
    return SplitIndices(
        f"scenario_holdout_{holdout_family}",
        train_idx.tolist(),
        val_idx.tolist(),
        list(map(int, test_idx)),
        {
            "holdout_family": holdout_family,
            "seed": seed,
            "benign_rest": len(benign_rest),
            "train_val_stratified": stratified,
            "train_val_pool_class_summary": class_summary,
        },
    )


def endpoint_pair_holdout_split(df: pd.DataFrame, seed: int = 42) -> SplitIndices:
    required = ["src_ip", "dst_ip", "dst_port", "protocol"]
    if not all(c in df.columns for c in required):
        raise ValueError(f"Endpoint holdout requires {required}")
    groups = (
        df["src_ip"].astype(str)
        + "|"
        + df["dst_ip"].astype(str)
        + "|"
        + df["dst_port"].astype(str)
        + "|"
        + df["protocol"].astype(str)
    )
    gss = GroupShuffleSplit(n_splits=1, train_size=0.70, random_state=seed)
    train_idx, tmp_idx = next(gss.split(df, groups=groups))
    tmp_df = df.iloc[tmp_idx]
    tmp_groups = groups.iloc[tmp_idx]
    gss2 = GroupShuffleSplit(n_splits=1, train_size=0.50, random_state=seed)
    val_rel, test_rel = next(gss2.split(tmp_df, groups=tmp_groups))
    return SplitIndices(
        "endpoint_pair_holdout",
        df.index[train_idx].to_list(),
        tmp_df.index[val_rel].to_list(),
        tmp_df.index[test_rel].to_list(),
        {"seed": seed},
    )


def open_set_holdout_split(df: pd.DataFrame, unknown_family: str, seed: int = 42) -> SplitIndices:
    split = scenario_holdout_split(df, unknown_family, seed)
    return SplitIndices(
        f"open_set_{unknown_family}",
        split.train_idx,
        split.val_idx,
        split.test_idx,
        {"unknown_family": unknown_family, "seed": seed},
    )

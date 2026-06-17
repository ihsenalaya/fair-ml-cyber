"""Model training helpers."""

from __future__ import annotations

import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import HistGradientBoostingClassifier, IsolationForest, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import LocalOutlierFactor
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


@dataclass
class FitResult:
    model_name: str
    model: Any
    train_seconds: float
    inference_seconds: float
    y_pred: np.ndarray
    y_prob: np.ndarray | None
    warning_count: int
    convergence_warning_count: int
    warning_messages: list[str]


def build_model(model_name: str, seed: int = 42) -> Any:
    if model_name == "logistic_regression":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        n_jobs=-1,
                        random_state=seed,
                    ),
                ),
            ]
        )
    if model_name == "random_forest":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=120,
                        max_depth=None,
                        min_samples_leaf=2,
                        class_weight="balanced_subsample",
                        n_jobs=-1,
                        random_state=seed,
                    ),
                ),
            ]
        )
    if model_name == "hist_gradient_boosting":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        max_iter=150,
                        learning_rate=0.08,
                        random_state=seed,
                    ),
                ),
            ]
        )
    if model_name == "mlp":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "model",
                    MLPClassifier(
                        hidden_layer_sizes=(64, 32),
                        max_iter=80,
                        early_stopping=True,
                        random_state=seed,
                    ),
                ),
            ]
        )
    if model_name == "isolation_forest":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    IsolationForest(
                        n_estimators=150,
                        contamination="auto",
                        n_jobs=-1,
                        random_state=seed,
                    ),
                ),
            ]
        )
    if model_name == "local_outlier_factor":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "model",
                    LocalOutlierFactor(
                        n_neighbors=35,
                        novelty=True,
                        contamination="auto",
                        n_jobs=-1,
                    ),
                ),
            ]
        )
    if model_name == "one_class_svm":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", OneClassSVM(gamma="scale", nu=0.05)),
            ]
        )
    raise ValueError(f"Unknown model: {model_name}")


def is_open_set_model(model_name: str) -> bool:
    return model_name in {"isolation_forest", "local_outlier_factor", "one_class_svm"}


def fit_predict(
    model_name: str,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    seed: int = 42,
) -> FitResult:
    model = build_model(model_name, seed)
    train_start = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        if is_open_set_model(model_name):
            benign_mask = y_train.astype(int) == 0
            model.fit(X_train.loc[benign_mask])
        else:
            model.fit(X_train, y_train)
    train_seconds = time.perf_counter() - train_start
    warning_messages = [str(w.message) for w in caught_warnings]
    convergence_warning_count = sum(
        1 for w in caught_warnings if issubclass(w.category, ConvergenceWarning)
    )

    infer_start = time.perf_counter()
    if is_open_set_model(model_name):
        raw_pred = model.predict(X_test)
        y_pred = (raw_pred == -1).astype(int)
        scores = -model.decision_function(X_test)
        y_prob = (scores - scores.min()) / (scores.max() - scores.min() + 1e-12)
    else:
        y_pred = model.predict(X_test)
        y_prob = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_test)
            if proba.shape[1] == 2:
                y_prob = proba[:, 1]
    inference_seconds = time.perf_counter() - infer_start
    return FitResult(
        model_name,
        model,
        train_seconds,
        inference_seconds,
        y_pred,
        y_prob,
        len(caught_warnings),
        convergence_warning_count,
        warning_messages,
    )


def save_model(model: Any, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier


def make_old_model(model_name: str):
    if model_name == "OLD1":
        estimator = DecisionTreeClassifier(
            criterion="entropy",
            max_depth=10,
            min_samples_leaf=1,
            min_samples_split=2,
            random_state=2026,
        )
    elif model_name == "OLD2":
        estimator = RandomForestClassifier(
            n_estimators=200,
            criterion="entropy",
            max_depth=15,
            min_samples_leaf=2,
            min_samples_split=4,
            random_state=2026,
            n_jobs=-1,
        )
    elif model_name == "OLD3":
        estimator = XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.03,
            subsample=0.8,
            objective="multi:softprob",
            eval_metric="mlogloss",
            random_state=1992,
            n_jobs=1,
            tree_method="hist",
        )
    else:
        raise ValueError(f"Unknown old model: {model_name}")
    return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", estimator)])


def make_xgb_binary(
    n_estimators: int,
    max_depth: int,
    learning_rate: float,
    subsample: float,
    random_state: int,
) -> Pipeline:
    estimator = XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=subsample,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        n_jobs=1,
        tree_method="hist",
    )
    return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", estimator)])


def make_new1_member() -> Pipeline:
    return make_xgb_binary(
        n_estimators=450,
        max_depth=3,
        learning_rate=0.03,
        subsample=0.8,
        random_state=20260618,
    )


def make_new2_member() -> Pipeline:
    return make_xgb_binary(
        n_estimators=300,
        max_depth=2,
        learning_rate=0.04,
        subsample=0.8,
        random_state=20260618,
    )


def encode_binary_label(y: pd.Series, positive_label: str = "Risk") -> np.ndarray:
    return (y.astype(str) == positive_label).astype(int).to_numpy()


def risk_probability_from_pipeline(model: Pipeline, x: pd.DataFrame) -> np.ndarray:
    proba = model.predict_proba(x)
    estimator = model.named_steps["model"]
    if hasattr(estimator, "classes_"):
        classes = list(estimator.classes_)
        if 1 in classes:
            return proba[:, classes.index(1)]
    return proba[:, -1]


def fit_old_model(model, x_train: pd.DataFrame, y_train: pd.Series):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_train.astype(str))
    model.fit(x_train, y_encoded)
    return label_encoder


def predict_old_model(model, label_encoder: LabelEncoder, x: pd.DataFrame) -> np.ndarray:
    encoded = model.predict(x)
    return label_encoder.inverse_transform(encoded.astype(int))


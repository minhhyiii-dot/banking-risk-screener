from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)


def binary_metrics(y_true: pd.Series, y_pred: pd.Series, positive_label: str = "Risk") -> dict[str, Any]:
    labels = [positive_label, "NoRisk"] if positive_label == "Risk" else sorted(pd.unique(y_true))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "per_class": {
            label: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i, label in enumerate(labels)
        },
        "confusion_matrix": {
            "labels": labels,
            "matrix": confusion_matrix(y_true, y_pred, labels=labels).astype(int).tolist(),
        },
    }


def multiclass_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, Any]:
    labels = sorted(pd.unique(pd.concat([pd.Series(y_true), pd.Series(y_pred)], ignore_index=True)))
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "classification_report": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        "confusion_matrix": {
            "labels": labels,
            "matrix": confusion_matrix(y_true, y_pred, labels=labels).astype(int).tolist(),
        },
    }


def save_json(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def threshold_predictions(probability: np.ndarray | pd.Series, threshold: float) -> np.ndarray:
    probability = np.asarray(probability, dtype=float)
    return np.where(probability >= threshold, "Risk", "NoRisk")


def threshold_sweep(
    y_true: pd.Series,
    risk_probability: np.ndarray | pd.Series,
    min_threshold: float = 0.2,
    max_threshold: float = 0.5,
    step: float = 0.001,
    min_risk_recall: float | None = None,
) -> pd.DataFrame:
    rows = []
    thresholds = np.round(np.arange(min_threshold, max_threshold + step / 2, step), 6)
    for threshold in thresholds:
        y_pred = threshold_predictions(risk_probability, float(threshold))
        m = binary_metrics(y_true, pd.Series(y_pred, index=y_true.index))
        risk = m["per_class"]["Risk"]
        norisk = m["per_class"]["NoRisk"]
        row = {
            "threshold": float(threshold),
            "accuracy": m["accuracy"],
            "balanced_accuracy": m["balanced_accuracy"],
            "macro_f1": m["macro_f1"],
            "risk_precision": risk["precision"],
            "risk_recall": risk["recall"],
            "risk_f1": risk["f1"],
            "norisk_precision": norisk["precision"],
            "norisk_recall": norisk["recall"],
            "norisk_f1": norisk["f1"],
        }
        if min_risk_recall is None or row["risk_recall"] >= min_risk_recall:
            rows.append(row)
    return pd.DataFrame(rows)


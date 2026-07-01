from __future__ import annotations

import numpy as np
import pandas as pd

from .data import load_common_master, new1_test_splits, new1_validation_splits
from .features import assert_no_known_leakage, get_new_feature_sets
from .metrics import binary_metrics, save_json, threshold_predictions, threshold_sweep
from .models import encode_binary_label, make_new1_member, risk_probability_from_pipeline
from .paths import OUTPUT_DIR


RAPIDMINER_THRESHOLD = 0.437


def _fit_member(train: pd.DataFrame, features: list[str], weight_column: str):
    model = make_new1_member()
    y_train = encode_binary_label(train["aux_risk5_label"])
    sample_weight = train[weight_column].astype(float).to_numpy()
    model.fit(train[features], y_train, model__sample_weight=sample_weight)
    return model


def _score_new1(train: pd.DataFrame, score: pd.DataFrame, features_258: list[str], features_309: list[str]):
    member_258 = _fit_member(train, features_258, "mg002_distance_weight")
    member_309 = _fit_member(train, features_309, "mg035_positive_weight")
    prob_258 = risk_probability_from_pipeline(member_258, score[features_258])
    prob_309 = risk_probability_from_pipeline(member_309, score[features_309])
    ensemble = 0.5 * prob_258 + 0.5 * prob_309
    return prob_258, prob_309, ensemble


def run_new1() -> dict:
    df = load_common_master()
    features_258, features_309 = get_new_feature_sets(df)
    assert_no_known_leakage(features_258)
    assert_no_known_leakage(features_309)

    val_train, validation = new1_validation_splits(df)
    val_prob_258, val_prob_309, val_ensemble = _score_new1(
        val_train, validation, features_258, features_309
    )
    sweep = threshold_sweep(
        validation["risk10_label"],
        val_ensemble,
        min_threshold=0.2,
        max_threshold=0.5,
        step=0.001,
        min_risk_recall=0.4,
    )
    if len(sweep) > 0:
        best_row = sweep.sort_values(
            ["accuracy", "norisk_recall", "threshold"],
            ascending=[False, False, True],
        ).iloc[0].to_dict()
        selected_threshold = float(best_row["threshold"])
    else:
        best_row = {}
        selected_threshold = RAPIDMINER_THRESHOLD

    final_train, test = new1_test_splits(df)
    test_prob_258, test_prob_309, test_ensemble = _score_new1(
        final_train, test, features_258, features_309
    )

    validation_pred_reference = threshold_predictions(val_ensemble, RAPIDMINER_THRESHOLD)
    validation_pred_selected = threshold_predictions(val_ensemble, selected_threshold)
    test_pred_reference = threshold_predictions(test_ensemble, RAPIDMINER_THRESHOLD)
    test_pred_selected = threshold_predictions(test_ensemble, selected_threshold)

    out_dir = OUTPUT_DIR / "NEW1"
    out_dir.mkdir(parents=True, exist_ok=True)
    sweep.to_csv(out_dir / "new1_validation_threshold_sweep.csv", index=False)
    pd.Series(features_258, name="feature").to_csv(out_dir / "new1_features_258.csv", index=False)
    pd.Series(features_309, name="feature").to_csv(out_dir / "new1_features_309.csv", index=False)

    validation_export = validation[
        ["row_key", "ticker", "feature_quarter", "target_quarter", "risk10_label", "aux_risk5_label"]
    ].copy()
    validation_export["probability_258"] = val_prob_258
    validation_export["probability_309"] = val_prob_309
    validation_export["ensemble_probability"] = val_ensemble
    validation_export["prediction_threshold_0_437"] = validation_pred_reference
    validation_export["prediction_selected_threshold"] = validation_pred_selected
    validation_export.to_csv(out_dir / "new1_validation_predictions.csv", index=False)

    test_export = test[["row_key", "ticker", "feature_quarter", "target_quarter", "risk10_label", "aux_risk5_label"]].copy()
    test_export["probability_258"] = test_prob_258
    test_export["probability_309"] = test_prob_309
    test_export["ensemble_probability"] = test_ensemble
    test_export["prediction_threshold_0_437"] = test_pred_reference
    test_export["prediction_selected_threshold"] = test_pred_selected
    test_export.to_csv(out_dir / "new1_test_predictions.csv", index=False)

    metrics = {
        "model": "NEW1",
        "task": "binary earnings-risk screening",
        "python_estimator_note": "XGBoostClassifier approximates RapidMiner/H2O GBT; exact binary identity is not expected.",
        "feature_counts": {
            "member_258": len(features_258),
            "member_309": len(features_309),
            "union": len(set(features_258) | set(features_309)),
            "overlap": len(set(features_258) & set(features_309)),
        },
        "split_counts": {
            "validation_train": int(len(val_train)),
            "validation": int(len(validation)),
            "final_train": int(len(final_train)),
            "test": int(len(test)),
        },
        "thresholds": {
            "rapidminer_reference": RAPIDMINER_THRESHOLD,
            "python_validation_selected": selected_threshold,
            "python_validation_best_row": best_row,
        },
        "validation_at_rapidminer_threshold": binary_metrics(
            validation["risk10_label"], pd.Series(validation_pred_reference, index=validation.index)
        ),
        "validation_at_python_selected_threshold": binary_metrics(
            validation["risk10_label"], pd.Series(validation_pred_selected, index=validation.index)
        ),
        "test_at_rapidminer_threshold": binary_metrics(
            test["risk10_label"], pd.Series(test_pred_reference, index=test.index)
        ),
        "test_at_python_selected_threshold": binary_metrics(
            test["risk10_label"], pd.Series(test_pred_selected, index=test.index)
        ),
    }
    save_json(metrics, out_dir / "new1_metrics.json")
    return metrics


if __name__ == "__main__":
    run_new1()


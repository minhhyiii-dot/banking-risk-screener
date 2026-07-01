from __future__ import annotations

import pandas as pd

from .data import load_pq_dataset
from .features import assert_no_known_leakage, get_pq_feature_sets
from .metrics import binary_metrics, save_json, threshold_predictions
from .models import encode_binary_label, make_new2_member, risk_probability_from_pipeline
from .paths import OUTPUT_DIR


THRESHOLDS = {
    "validation": 0.3210824176669121,
    "test": 0.331,
}


def _fit_pq_member(train: pd.DataFrame, features: list[str]):
    model = make_new2_member()
    y_train = encode_binary_label(train["risk10_label"])
    sample_weight = train["pq_sample_weight"].astype(float).to_numpy()
    model.fit(train[features], y_train, model__sample_weight=sample_weight)
    return model


def run_new2(kind: str = "test") -> dict:
    df = load_pq_dataset(kind)
    features_258, features_309 = get_pq_feature_sets(df)
    assert_no_known_leakage(features_258)
    assert_no_known_leakage(features_309)

    threshold = THRESHOLDS[kind]
    prediction_rows = []
    quarter_metrics = []

    for evaluation_quarter, group in df.groupby("evaluation_target_quarter", sort=True):
        train = group[group["pq_role"] == "train"].copy()
        score = group[group["pq_role"] == "score"].copy()
        if train.empty or score.empty:
            continue

        member_258 = _fit_pq_member(train, features_258)
        member_309 = _fit_pq_member(train, features_309)
        prob_258 = risk_probability_from_pipeline(member_258, score[features_258])
        prob_309 = risk_probability_from_pipeline(member_309, score[features_309])
        ensemble = 0.75 * prob_258 + 0.25 * prob_309
        pred = threshold_predictions(ensemble, threshold)

        export = score[["row_key", "ticker", "feature_quarter", "target_quarter", "risk10_label"]].copy()
        export["evaluation_target_quarter"] = evaluation_quarter
        export["probability_pq006"] = prob_258
        export["probability_pq012"] = prob_309
        export["ensemble_probability"] = ensemble
        export["prediction_pq087"] = pred
        prediction_rows.append(export)

        quarter_metrics.append(
            {
                "evaluation_target_quarter": evaluation_quarter,
                "train_rows": int(len(train)),
                "score_rows": int(len(score)),
                "risk_score_rows": int((score["risk10_label"] == "Risk").sum()),
            }
        )

    predictions = pd.concat(prediction_rows, ignore_index=True) if prediction_rows else pd.DataFrame()
    out_dir = OUTPUT_DIR / "NEW2" / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(out_dir / f"new2_{kind}_predictions.csv", index=False)
    pd.DataFrame(quarter_metrics).to_csv(out_dir / f"new2_{kind}_quarter_windows.csv", index=False)
    pd.Series(features_258, name="feature").to_csv(out_dir / "new2_features_258.csv", index=False)
    pd.Series(features_309, name="feature").to_csv(out_dir / "new2_features_309.csv", index=False)

    metrics = {
        "model": "NEW2",
        "kind": kind,
        "task": "prequential binary earnings-risk screening",
        "python_estimator_note": "XGBoostClassifier approximates RapidMiner/H2O GBT; exact binary identity is not expected.",
        "threshold": threshold,
        "feature_counts": {
            "member_258": len(features_258),
            "member_309": len(features_309),
            "union": len(set(features_258) | set(features_309)),
            "overlap": len(set(features_258) & set(features_309)),
        },
        "input_rows": int(len(df)),
        "score_rows": int(len(predictions)),
        "evaluation_quarters": int(len(quarter_metrics)),
        "performance": binary_metrics(
            predictions["risk10_label"], predictions["prediction_pq087"]
        )
        if len(predictions)
        else {},
    }
    save_json(metrics, out_dir / f"new2_{kind}_metrics.json")
    return metrics


if __name__ == "__main__":
    run_new2("validation")
    run_new2("test")


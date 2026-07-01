from __future__ import annotations

import pandas as pd

from .data import load_old_master, old_splits
from .features import assert_no_known_leakage, get_old_feature_set
from .metrics import multiclass_metrics, save_json
from .models import fit_old_model, make_old_model, predict_old_model
from .paths import OUTPUT_DIR


def evaluate_one_old_model(model_name: str) -> dict:
    df = load_old_master()
    features = get_old_feature_set(df)
    assert_no_known_leakage(features)

    train, validation, test = old_splits(df)
    model = make_old_model(model_name)
    encoder = fit_old_model(model, train[features], train["segment_label"])

    rows = []
    metrics = {
        "model": model_name,
        "task": "archived Growth/Safe/Risky multiclass task",
        "feature_count": len(features),
        "split_counts": {
            "train": int(len(train)),
            "validation": int(len(validation)),
            "test": int(len(test)),
        },
    }

    for split_name, split_df in [("validation", validation), ("test", test)]:
        pred = predict_old_model(model, encoder, split_df[features])
        split_metrics = multiclass_metrics(split_df["segment_label"], pd.Series(pred, index=split_df.index))
        metrics[split_name] = split_metrics

        export = split_df[["bank_quarter_id", "ticker", "report_year", "report_quarter", "segment_label"]].copy()
        export["prediction"] = pred
        export["split"] = split_name
        rows.append(export)

    out_dir = OUTPUT_DIR / model_name
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.concat(rows, ignore_index=True).to_csv(out_dir / f"{model_name.lower()}_predictions.csv", index=False)
    pd.Series(features, name="feature").to_csv(out_dir / f"{model_name.lower()}_features.csv", index=False)
    save_json(metrics, out_dir / f"{model_name.lower()}_metrics.json")
    return metrics


def run_old_models() -> dict[str, dict]:
    results = {}
    for model_name in ["OLD1", "OLD2", "OLD3"]:
        results[model_name] = evaluate_one_old_model(model_name)
    save_json(results, OUTPUT_DIR / "old_models_summary.json")
    return results


if __name__ == "__main__":
    run_old_models()


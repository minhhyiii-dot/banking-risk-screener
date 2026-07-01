from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR / "src"))

from banking_risk_pipeline.data import (
    load_common_master,
    load_old_master,
    load_pq_dataset,
    new1_test_splits,
    new1_validation_splits,
    old_splits,
)
from banking_risk_pipeline.paths import OUTPUT_DIR


def distribution(series: pd.Series) -> dict:
    counts = series.astype(str).value_counts(dropna=False).sort_index()
    total = int(counts.sum())
    return {
        "total": total,
        "counts": {str(k): int(v) for k, v in counts.items()},
        "rates": {str(k): float(v / total) for k, v in counts.items()},
    }


def main() -> None:
    rows = []
    report = {}

    old = load_old_master()
    for split_name, split_df in zip(["train", "validation", "test"], old_splits(old)):
        key = f"old_{split_name}_segment_label"
        report[key] = distribution(split_df["segment_label"])
        for label, count in report[key]["counts"].items():
            rows.append({"dataset": "old_master", "split": split_name, "label_column": "segment_label", "label": label, "count": count, "rate": report[key]["rates"][label]})

    common = load_common_master()
    val_train, validation = new1_validation_splits(common)
    final_train, test = new1_test_splits(common)
    common_splits = {
        "validation_train": val_train,
        "validation": validation,
        "final_train": final_train,
        "test": test,
    }
    for split_name, split_df in common_splits.items():
        for label_column in ["risk10_label", "aux_risk5_label"]:
            key = f"new1_{split_name}_{label_column}"
            report[key] = distribution(split_df[label_column])
            for label, count in report[key]["counts"].items():
                rows.append({"dataset": "common_master", "split": split_name, "label_column": label_column, "label": label, "count": count, "rate": report[key]["rates"][label]})

    for kind in ["validation", "test"]:
        pq = load_pq_dataset(kind)
        score = pq[pq["pq_role"] == "score"]
        train = pq[pq["pq_role"] == "train"]
        for split_name, split_df in [(f"{kind}_train_expanded", train), (f"{kind}_score", score)]:
            key = f"new2_{split_name}_risk10_label"
            report[key] = distribution(split_df["risk10_label"])
            for label, count in report[key]["counts"].items():
                rows.append({"dataset": f"pq_{kind}", "split": split_name, "label_column": "risk10_label", "label": label, "count": count, "rate": report[key]["rates"][label]})

    out_dir = OUTPUT_DIR / "class_distribution"
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_dir / "class_distribution_summary.csv", index=False)
    (out_dir / "class_distribution_summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote outputs/python_baseline/class_distribution")


if __name__ == "__main__":
    main()

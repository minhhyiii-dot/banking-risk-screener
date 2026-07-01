from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from .rmp_specs import load_rmp_specs, operator_subset


NON_FEATURE_COLUMNS = {
    "row_key",
    "bank_quarter_id",
    "ticker",
    "report_year",
    "report_quarter",
    "quarter_label",
    "period_end",
    "period_end_date",
    "asof_trade_date",
    "exchange",
    "feature_quarter",
    "target_year",
    "target_quarter_number",
    "target_q_index",
    "target_quarter",
    "quarter_index",
    "risk10_numeric",
    "risk10_label",
    "aux_risk5_numeric",
    "aux_risk5_label",
    "mg002_distance_weight",
    "mg035_positive_weight",
    "pq_sample_weight",
    "pq_age_years",
    "pq_role",
    "evaluation_target_q_index",
    "evaluation_target_quarter",
    "segment_label",
}


def clean_feature_list(columns: Iterable[str], available_columns: Iterable[str]) -> list[str]:
    available = set(available_columns)
    cleaned: list[str] = []
    for column in columns:
        column = column.replace("ï»¿", "").replace("\ufeff", "").strip()
        if not column or column in NON_FEATURE_COLUMNS:
            continue
        if column not in available:
            continue
        if column not in cleaned:
            cleaned.append(column)
    return cleaned


def get_old_feature_set(df: pd.DataFrame) -> list[str]:
    specs = load_rmp_specs()
    old_key = next(k for k in specs if "model OLD1" in k)
    raw = operator_subset(specs[old_key], "Select Attributes (3)")
    return clean_feature_list(raw, df.columns)


def get_new_feature_sets(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    specs = load_rmp_specs()
    new1_key = next(k for k in specs if "model NEW1" in k)
    raw_258 = operator_subset(specs[new1_key], "Select Attributes (VT258)")
    raw_309 = operator_subset(specs[new1_key], "Select Attributes (VT309)")
    return clean_feature_list(raw_258, df.columns), clean_feature_list(raw_309, df.columns)


def get_pq_feature_sets(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    specs = load_rmp_specs()
    pq_key = next(k for k in specs if "model NEW2" in k and "test" in k)
    raw_258 = operator_subset(specs[pq_key], "Select PQ006 258 Features")
    raw_309 = operator_subset(specs[pq_key], "Select PQ012 309 Features")
    return clean_feature_list(raw_258, df.columns), clean_feature_list(raw_309, df.columns)


def assert_no_known_leakage(feature_columns: list[str]) -> None:
    leaked = [
        col
        for col in feature_columns
        if col.startswith("next_quarter")
        or col in {"risk10_label", "risk10_numeric", "aux_risk5_label", "aux_risk5_numeric"}
    ]
    if leaked:
        raise ValueError(f"Potential leakage columns in feature set: {leaked[:20]}")


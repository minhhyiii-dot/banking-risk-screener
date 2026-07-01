from __future__ import annotations

import pandas as pd

from .paths import COMMON_MASTER_PATH, OLD_MASTER_PATH, PQ_TEST_PATH, PQ_VALIDATION_PATH


def read_csv_clean(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.replace("\ufeff", "").replace("ï»¿", "").strip() for c in df.columns]
    return df


def load_old_master() -> pd.DataFrame:
    return read_csv_clean(OLD_MASTER_PATH)


def load_common_master() -> pd.DataFrame:
    return read_csv_clean(COMMON_MASTER_PATH)


def load_pq_dataset(kind: str) -> pd.DataFrame:
    if kind == "validation":
        return read_csv_clean(PQ_VALIDATION_PATH)
    if kind == "test":
        return read_csv_clean(PQ_TEST_PATH)
    raise ValueError("kind must be 'validation' or 'test'")


def old_splits(df: pd.DataFrame):
    train = df[(df["report_year"] >= 2016) & (df["report_year"] <= 2022)].copy()
    validation = df[df["report_year"] == 2023].copy()
    test = df[(df["report_year"] >= 2024) & (df["report_year"] <= 2025)].copy()
    return train, validation, test


def new1_validation_splits(df: pd.DataFrame):
    train = df[df["target_year"] < 2020].copy()
    validation = df[(df["target_year"] >= 2020) & (df["target_year"] <= 2023)].copy()
    return train, validation


def new1_test_splits(df: pd.DataFrame):
    train = df[df["target_year"] < 2024].copy()
    test = df[df["target_year"] >= 2024].copy()
    return train, test


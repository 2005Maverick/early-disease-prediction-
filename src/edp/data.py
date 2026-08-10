"""Data layer: loading and honest handling of hidden missing values.

Config-driven: each disease declares its dataset, feature list, and which
columns hide missing values as impossible zeros (the famous Pima trap - a
zero blood sugar is not a measurement, it is a hole in the data). Values are
marked missing here; the pipelines impute per training fold (no leakage).
"""
from pathlib import Path

import numpy as np
import pandas as pd

from edp.diseases.base import DiseaseConfig


def load_raw(config: DiseaseConfig, root: str | Path = '.') -> pd.DataFrame:
    """Load a disease's dataset and validate its shape and columns."""
    df = pd.read_csv(Path(root) / config.dataset)
    missing_cols = (set(config.features) | {config.target}) - set(df.columns)
    if missing_cols:
        raise ValueError(f"{config.key}: dataset is missing columns "
                         f"{sorted(missing_cols)}")
    if df.empty:
        raise ValueError(f"{config.key}: dataset is empty")
    return df


def mark_missing(df: pd.DataFrame, config: DiseaseConfig) -> pd.DataFrame:
    """New frame with impossible zeros replaced by NaN (never mutates input)."""
    out = df.copy()
    for col in config.zero_missing:
        out[col] = out[col].replace(0, np.nan)
    return out


def load_clean(config: DiseaseConfig,
               root: str | Path = '.') -> tuple[pd.DataFrame, pd.Series]:
    """Load, mark hidden missing values, split into features X and target y."""
    df = mark_missing(load_raw(config, root), config)
    return df[list(config.features)], df[config.target]


def missingness_report(config: DiseaseConfig,
                       root: str | Path = '.') -> pd.DataFrame:
    """How many missing values each feature hides - shown in the Model Lab."""
    raw = mark_missing(load_raw(config, root), config)
    rows = [
        {'Feature': config.friendly.get(col, col),
         'Missing values': int(raw[col].isna().sum()),
         'Percent of patients': round(float(raw[col].isna().mean() * 100), 1)}
        for col in config.features if raw[col].isna().any()
    ]
    if not rows:
        rows = [{'Feature': '(none)', 'Missing values': 0,
                 'Percent of patients': 0.0}]
    return pd.DataFrame(rows)

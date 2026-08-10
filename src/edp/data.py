"""Data layer: loading and honest handling of the Pima dataset's hidden missing values.

The famous trap in this dataset: zeros in Glucose, BloodPressure, SkinThickness,
Insulin and BMI are physiologically impossible (nobody has zero blood sugar).
They are undocumented missing values. Most projects feed them to the model as
real numbers, silently distorting everything. We mark them as missing here and
let the pipeline impute them per training fold (no data leakage).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ALL_FEATURES: tuple[str, ...] = (
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age',
)
TARGET = 'Outcome'

# Zero is a valid value for Pregnancies; impossible for these five.
ZERO_MEANS_MISSING: tuple[str, ...] = (
    'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
)


def load_raw(csv_path: str | Path) -> pd.DataFrame:
    """Load the dataset and validate its shape and columns."""
    df = pd.read_csv(csv_path)
    missing_cols = (set(ALL_FEATURES) | {TARGET}) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing columns: {sorted(missing_cols)}")
    if df.empty:
        raise ValueError("Dataset is empty")
    return df


def mark_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return a new frame with impossible zeros replaced by NaN (never mutates input)."""
    out = df.copy()
    for col in ZERO_MEANS_MISSING:
        out[col] = out[col].replace(0, np.nan)
    return out


def load_clean(csv_path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load, mark hidden missing values, and split into features X and target y."""
    df = mark_missing(load_raw(csv_path))
    return df[list(ALL_FEATURES)], df[TARGET]


def missingness_report(csv_path: str | Path) -> pd.DataFrame:
    """How many 'impossible zeros' each column hides — used in the dashboard."""
    raw = load_raw(csv_path)
    rows = [
        {'Feature': col,
         'Hidden missing values': int((raw[col] == 0).sum()),
         'Percent of patients': round(float((raw[col] == 0).mean() * 100), 1)}
        for col in ZERO_MEANS_MISSING
    ]
    return pd.DataFrame(rows)

"""Explanation layer: personal risk drivers, without SHAP jargon.

One sentence for the professor: "For each health factor we ask — if this
patient had a typical (median) value here instead of their own, how much
would their risk fall? The drop is that factor's personal contribution."

Model-agnostic, exact for the deployed ensemble, and understandable by anyone.
"""
from typing import Callable, NamedTuple

import numpy as np
import pandas as pd


class Driver(NamedTuple):
    feature: str
    patient_value: float
    typical_value: float
    risk_delta: float  # patient risk minus risk-with-typical-value (>0 raises risk)


def compute_drivers(predict_mean: Callable[[pd.DataFrame], np.ndarray],
                    patient: pd.DataFrame,
                    typical: pd.Series) -> list[Driver]:
    """Risk contribution of each feature via median substitution.

    predict_mean: function mapping a feature frame to risk scores.
    patient: single-row frame with the patient's values.
    typical: per-feature medians of the study population.
    """
    if len(patient) != 1:
        raise ValueError("compute_drivers expects exactly one patient row")
    features = list(patient.columns)
    # Row 0 = patient as-is; row i = patient with feature i set to typical.
    rows = [patient.iloc[0].copy()]
    for feat in features:
        swapped = patient.iloc[0].copy()
        swapped[feat] = typical[feat]
        rows.append(swapped)
    batch = pd.DataFrame(rows).reset_index(drop=True)
    risks = predict_mean(batch)
    base = float(risks[0])
    drivers = [
        Driver(feature=feat,
               patient_value=float(patient.iloc[0][feat]),
               typical_value=float(typical[feat]),
               risk_delta=round(base - float(risks[i + 1]), 4))
        for i, feat in enumerate(features)
    ]
    return sorted(drivers, key=lambda d: d.risk_delta, reverse=True)

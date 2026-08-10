"""What-if simulator: re-score a patient under achievable changes.

Generic engine - each disease supplies its own scenario builder in its
config. One sentence: "change one number in the profile, run the model
again; the risk change shows what that change is worth."
"""
from typing import Callable, NamedTuple

import numpy as np
import pandas as pd


class Scenario(NamedTuple):
    label: str
    feature: str
    new_value: float


class ScenarioResult(NamedTuple):
    label: str
    new_risk: float
    risk_delta: float  # negative = risk reduced


def evaluate_scenarios(predict_mean: Callable[[pd.DataFrame], np.ndarray],
                       patient: pd.DataFrame,
                       scenarios: list[Scenario]) -> list[ScenarioResult]:
    """Score every scenario in one model call; the input frame is never mutated."""
    if not scenarios:
        return []
    rows = [patient.iloc[0].copy()]
    for sc in scenarios:
        changed = patient.iloc[0].copy()
        changed[sc.feature] = sc.new_value
        rows.append(changed)
    batch = pd.DataFrame(rows).reset_index(drop=True)
    risks = predict_mean(batch)
    base = float(risks[0])
    return [
        ScenarioResult(label=sc.label,
                       new_risk=round(float(risks[i + 1]), 4),
                       risk_delta=round(float(risks[i + 1]) - base, 4))
        for i, sc in enumerate(scenarios)
    ]

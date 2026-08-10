"""What-if simulator: re-score the patient under achievable lifestyle changes.

One sentence: "We change one number in the patient's profile — as if they had
lost weight or lowered glucose — and run the model again; the risk drop shows
what that change is worth."
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


def build_scenarios(patient: pd.DataFrame) -> list[Scenario]:
    """Only scenarios that make sense for this patient (never below healthy floors)."""
    if len(patient) != 1:
        raise ValueError("build_scenarios expects exactly one patient row")
    row = patient.iloc[0]
    scenarios: list[Scenario] = []
    bmi = float(row['BMI'])
    if not np.isnan(bmi) and bmi > 25:
        scenarios.append(Scenario('Lose weight: BMI -2', 'BMI', round(max(22.0, bmi - 2), 1)))
        if bmi - 5 >= 22:
            scenarios.append(Scenario('Lose weight: BMI -5', 'BMI', round(bmi - 5, 1)))
    glucose = float(row['Glucose'])
    if not np.isnan(glucose) and glucose > 110:
        scenarios.append(Scenario('Lower glucose by 15', 'Glucose', max(95.0, glucose - 15)))
        if glucose - 30 >= 95:
            scenarios.append(Scenario('Lower glucose by 30', 'Glucose', glucose - 30))
    insulin = float(row['Insulin'])
    if not np.isnan(insulin) and insulin > 160:
        scenarios.append(Scenario('Normalize insulin to 120', 'Insulin', 120.0))
    return scenarios


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

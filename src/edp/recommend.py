"""Preventive action plan: rules from published clinical reference ranges.

Deliberately NOT machine-learned: prevention advice must be traceable to a
medical guideline, not to a statistical artifact. Each rule cites the range
that triggered it, using the patient's own numbers.

Educational tool — not medical advice; the UI displays that disclaimer.
"""
from typing import NamedTuple

import numpy as np
import pandas as pd


class Recommendation(NamedTuple):
    title: str
    reason: str
    action: str


def build_recommendations(patient: pd.DataFrame, risk: float) -> list[Recommendation]:
    """Personalized, rule-based preventive actions for a single patient row."""
    if len(patient) != 1:
        raise ValueError("build_recommendations expects exactly one patient row")
    row = patient.iloc[0]
    recs: list[Recommendation] = []

    glucose = float(row['Glucose'])
    if not np.isnan(glucose):
        if glucose >= 200:
            recs.append(Recommendation(
                'See a doctor about blood sugar soon',
                f'A 2-hour glucose of {glucose:.0f} mg/dL is in the diabetic range (>= 200).',
                'Book a clinical consultation; an HbA1c test can confirm the picture.'))
        elif glucose >= 140:
            recs.append(Recommendation(
                'Reduce blood sugar',
                f'A 2-hour glucose of {glucose:.0f} mg/dL indicates impaired glucose '
                'tolerance (140-199).',
                'Cut sugary drinks and refined carbs; 30 minutes of brisk walking '
                'daily measurably lowers post-meal glucose.'))

    bmi = float(row['BMI'])
    if not np.isnan(bmi):
        if bmi >= 30:
            recs.append(Recommendation(
                'Weight reduction has the biggest payoff',
                f'A BMI of {bmi:.1f} is in the obese range (>= 30).',
                'A 5-7% weight loss cut diabetes incidence by 58% in the landmark '
                'Diabetes Prevention Program trial.'))
        elif bmi >= 25:
            recs.append(Recommendation(
                'Aim for a healthier weight',
                f'A BMI of {bmi:.1f} is in the overweight range (25-30).',
                'Even losing 3-5 kg meaningfully lowers diabetes risk.'))

    insulin = float(row['Insulin'])
    if not np.isnan(insulin) and insulin >= 160:
        recs.append(Recommendation(
            'Signs of insulin resistance',
            f'A 2-hour insulin of {insulin:.0f} mu U/ml is elevated.',
            'Strength training and reducing refined carbohydrates improve '
            'insulin sensitivity.'))

    age = float(row['Age'])
    if not np.isnan(age) and age >= 45:
        recs.append(Recommendation(
            'Screen regularly from age 45',
            f'At age {age:.0f}, guidelines recommend periodic screening.',
            'Test fasting glucose or HbA1c at least every 3 years - yearly if '
            'other risk factors are present.'))

    if not recs:
        recs.append(Recommendation(
            'Keep doing what you are doing',
            'All entered values are inside healthy reference ranges.',
            'Maintain current diet and activity; re-check risk yearly.'))
    if risk >= 0.5:
        recs.insert(0, Recommendation(
            'Discuss this result with a healthcare professional',
            f'The model estimates {risk * 100:.0f}% risk - well above the alert level.',
            'Early clinical follow-up is exactly what early prediction is for.'))
    return recs

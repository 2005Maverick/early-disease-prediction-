"""Diabetes (Pima study): config, what-if scenarios, and prevention rules."""
import numpy as np
import pandas as pd

from edp.diseases.base import DiseaseConfig
from edp.recommend import Recommendation
from edp.whatif import Scenario

FEATURES = ('Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age')


def build_scenarios(patient: pd.DataFrame) -> list[Scenario]:
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


def build_recommendations(patient: pd.DataFrame, risk: float) -> list[Recommendation]:
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


CONFIG = DiseaseConfig(
    key='diabetes',
    name='Diabetes',
    dataset='datasets/diabetes.csv',
    features=FEATURES,
    target='Outcome',
    zero_missing=('Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI'),
    friendly={'Pregnancies': 'Pregnancies', 'Glucose': 'Blood glucose',
              'BloodPressure': 'Blood pressure', 'SkinThickness': 'Skin thickness',
              'Insulin': 'Insulin', 'BMI': 'BMI',
              'DiabetesPedigreeFunction': 'Family history', 'Age': 'Age'},
    strip_fields=(('Glucose', 'Glucose'), ('BMI', 'BMI'), ('Age', 'Age'),
                  ('BloodPressure', 'Blood pressure'), ('Insulin', 'Insulin'),
                  ('Pregnancies', 'Pregnancies'),
                  ('DiabetesPedigreeFunction', 'Family history')),
    similar_axes=(('Glucose', 'Blood glucose (mg/dL)'), ('BMI', 'BMI')),
    form_spec=(
        {'kind': 'number', 'col': 'Glucose', 'label': 'Glucose (2h OGTT, mg/dL)',
         'min': 40, 'max': 300, 'default': 120},
        {'kind': 'number', 'col': 'BMI', 'label': 'BMI', 'min': 15.0, 'max': 70.0,
         'default': 30.0, 'step': 0.1, 'format': '%.1f'},
        {'kind': 'number', 'col': 'Age', 'label': 'Age (years)', 'min': 18,
         'max': 100, 'default': 33},
        {'kind': 'number', 'col': 'BloodPressure',
         'label': 'Blood pressure (diastolic, mm Hg)', 'min': 30, 'max': 140,
         'default': 70},
        {'kind': 'number', 'col': 'Pregnancies', 'label': 'Pregnancies',
         'min': 0, 'max': 20, 'default': 2},
        {'kind': 'number', 'col': 'DiabetesPedigreeFunction',
         'label': 'Family history score (pedigree)', 'min': 0.0, 'max': 2.5,
         'default': 0.4, 'step': 0.01, 'format': '%.2f',
         'help': 'Higher = more relatives with diabetes'},
        {'kind': 'number_unknown', 'col': 'Insulin',
         'label': 'Insulin (2h serum, mu U/ml)', 'min': 10, 'max': 900,
         'default': 100},
        {'kind': 'number_unknown', 'col': 'SkinThickness',
         'label': 'Skin thickness (mm)', 'min': 5, 'max': 100, 'default': 25,
         'unknown_default': True},
    ),
    build_scenarios=build_scenarios,
    build_recommendations=build_recommendations,
    dataset_note='Pima study, 768 patients (National Institute of Diabetes '
                 'and Digestive and Kidney Diseases)',
)

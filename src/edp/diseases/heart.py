"""Heart disease (UCI Cleveland study): config, scenarios, prevention rules."""
import numpy as np
import pandas as pd

from edp.diseases.base import DiseaseConfig
from edp.recommend import Recommendation
from edp.whatif import Scenario

FEATURES = ('Age', 'Sex', 'ChestPain', 'RestingBP', 'Cholesterol', 'FastingBS',
            'RestECG', 'MaxHeartRate', 'ExerciseAngina', 'STDepression',
            'Slope', 'MajorVessels', 'Thallium')


def build_scenarios(patient: pd.DataFrame) -> list[Scenario]:
    row = patient.iloc[0]
    scenarios: list[Scenario] = []
    chol = float(row['Cholesterol'])
    if not np.isnan(chol) and chol > 200:
        scenarios.append(Scenario('Lower cholesterol by 30', 'Cholesterol',
                                  max(170.0, chol - 30)))
        if chol - 60 >= 170:
            scenarios.append(Scenario('Lower cholesterol by 60', 'Cholesterol',
                                      chol - 60))
    bp = float(row['RestingBP'])
    if not np.isnan(bp) and bp > 130:
        scenarios.append(Scenario('Lower resting BP by 10', 'RestingBP',
                                  max(115.0, bp - 10)))
        if bp - 20 >= 115:
            scenarios.append(Scenario('Lower resting BP by 20', 'RestingBP',
                                      bp - 20))
    return scenarios


def build_recommendations(patient: pd.DataFrame, risk: float) -> list[Recommendation]:
    row = patient.iloc[0]
    recs: list[Recommendation] = []
    chol = float(row['Cholesterol'])
    if not np.isnan(chol):
        if chol >= 240:
            recs.append(Recommendation(
                'Bring cholesterol down',
                f'Total cholesterol of {chol:.0f} mg/dL is in the high range (>= 240).',
                'Discuss lipid management with a doctor; diet change and statins '
                'are both well-evidenced.'))
        elif chol >= 200:
            recs.append(Recommendation(
                'Watch cholesterol',
                f'Total cholesterol of {chol:.0f} mg/dL is borderline high (200-239).',
                'More soluble fiber and less saturated fat measurably lower LDL.'))
    bp = float(row['RestingBP'])
    if not np.isnan(bp):
        if bp >= 140:
            recs.append(Recommendation(
                'Blood pressure needs attention',
                f'A resting blood pressure of {bp:.0f} mm Hg is stage-2 '
                'hypertension (>= 140).',
                'Home monitoring plus a clinical consultation; salt reduction and '
                'regular aerobic exercise both lower systolic pressure.'))
        elif bp >= 130:
            recs.append(Recommendation(
                'Slightly elevated blood pressure',
                f'A resting blood pressure of {bp:.0f} mm Hg is stage-1 '
                'hypertension (130-139).',
                'The DASH diet and 150 min/week of moderate exercise are '
                'first-line, guideline-backed steps.'))
    if float(row['ExerciseAngina']) == 1:
        recs.append(Recommendation(
            'Chest pain on exertion deserves a check-up',
            'Exercise-induced angina was reported.',
            'A clinician can order a stress test; do not push through exertional '
            'chest pain in the meantime.'))
    if float(row['FastingBS']) == 1:
        recs.append(Recommendation(
            'Elevated fasting blood sugar',
            'Fasting blood sugar above 120 mg/dL was reported.',
            'Screen for diabetes - the two conditions share risk factors and '
            'compound each other.'))
    age = float(row['Age'])
    sex = float(row['Sex'])
    if not np.isnan(age) and (age >= 45 if sex == 1 else age >= 55):
        recs.append(Recommendation(
            'Age is a risk factor - screen periodically',
            f'At age {age:.0f}, guidelines recommend regular cardiovascular '
            'risk assessment.',
            'Blood pressure yearly; lipid panel every 4-6 years, more often '
            'with other risk factors.'))
    if not recs:
        recs.append(Recommendation(
            'Keep doing what you are doing',
            'All entered values are inside healthy reference ranges.',
            'Maintain current activity and diet; re-check risk yearly.'))
    if risk >= 0.5:
        recs.insert(0, Recommendation(
            'Discuss this result with a healthcare professional',
            f'The model estimates {risk * 100:.0f}% risk - well above the alert level.',
            'Early clinical follow-up is exactly what early prediction is for.'))
    return recs


CONFIG = DiseaseConfig(
    key='heart',
    name='Heart disease',
    dataset='datasets/heart.csv',
    features=FEATURES,
    target='Outcome',
    zero_missing=(),  # the Cleveland file marks missing with '?', already NaN
    friendly={'Age': 'Age', 'Sex': 'Sex', 'ChestPain': 'Chest pain type',
              'RestingBP': 'Resting blood pressure', 'Cholesterol': 'Cholesterol',
              'FastingBS': 'Fasting blood sugar', 'RestECG': 'Resting ECG',
              'MaxHeartRate': 'Max heart rate', 'ExerciseAngina': 'Exercise angina',
              'STDepression': 'ST depression', 'Slope': 'ST slope',
              'MajorVessels': 'Major vessels', 'Thallium': 'Thallium test'},
    strip_fields=(('Age', 'Age'), ('Cholesterol', 'Cholesterol'),
                  ('RestingBP', 'Resting BP'), ('MaxHeartRate', 'Max heart rate'),
                  ('STDepression', 'ST depression'), ('MajorVessels', 'Major vessels')),
    similar_axes=(('MaxHeartRate', 'Max heart rate (bpm)'), ('Age', 'Age (years)')),
    form_spec=(
        {'kind': 'number', 'col': 'Age', 'label': 'Age (years)', 'min': 18,
         'max': 100, 'default': 50},
        {'kind': 'select', 'col': 'Sex', 'label': 'Sex',
         'options': (('Female', 0), ('Male', 1)), 'default_index': 1},
        {'kind': 'select', 'col': 'ChestPain', 'label': 'Chest pain type',
         'options': (('Typical angina', 1), ('Atypical angina', 2),
                     ('Non-anginal pain', 3), ('No chest pain (asymptomatic)', 4)),
         'default_index': 3},
        {'kind': 'number', 'col': 'RestingBP',
         'label': 'Resting blood pressure (systolic, mm Hg)', 'min': 80,
         'max': 220, 'default': 130},
        {'kind': 'number', 'col': 'Cholesterol',
         'label': 'Total cholesterol (mg/dL)', 'min': 100, 'max': 600,
         'default': 230},
        {'kind': 'flag', 'col': 'FastingBS',
         'label': 'Fasting blood sugar above 120 mg/dL'},
        {'kind': 'number', 'col': 'MaxHeartRate',
         'label': 'Max heart rate achieved (bpm)', 'min': 60, 'max': 220,
         'default': 150, 'help': 'From an exercise/stress test'},
        {'kind': 'flag', 'col': 'ExerciseAngina',
         'label': 'Chest pain during exercise'},
        {'kind': 'number', 'col': 'STDepression',
         'label': 'ST depression (exercise ECG)', 'min': 0.0, 'max': 7.0,
         'default': 1.0, 'step': 0.1, 'format': '%.1f'},
        {'kind': 'select', 'col': 'RestECG', 'label': 'Resting ECG result',
         'options': (('Normal', 0), ('ST-T abnormality', 1),
                     ('Left ventricular hypertrophy', 2)), 'default_index': 0},
        {'kind': 'select', 'col': 'Slope', 'label': 'ST segment slope (exercise)',
         'options': (('Upsloping', 1), ('Flat', 2), ('Downsloping', 3)),
         'default_index': 1},
        {'kind': 'select_unknown', 'col': 'MajorVessels',
         'label': 'Major vessels colored (fluoroscopy)',
         'options': (('0', 0), ('1', 1), ('2', 2), ('3', 3)), 'default_index': 0},
        {'kind': 'select_unknown', 'col': 'Thallium', 'label': 'Thallium stress test',
         'options': (('Normal', 3), ('Fixed defect', 6), ('Reversible defect', 7)),
         'default_index': 0},
    ),
    build_scenarios=build_scenarios,
    build_recommendations=build_recommendations,
    dataset_note='Cleveland Clinic study, 303 patients (UCI Machine Learning '
                 'Repository)',
)

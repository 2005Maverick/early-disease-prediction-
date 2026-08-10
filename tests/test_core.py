"""Unit tests for the core layers (fast: pure logic, synthetic data)."""
import numpy as np
import pandas as pd
import pytest

from edp.data import mark_missing
from edp.diseases import REGISTRY
from edp.diseases.diabetes import CONFIG as DIABETES
from edp.diseases.heart import CONFIG as HEART
from edp.drivers import compute_drivers
from edp.risk import classify, select_threshold
from edp.whatif import evaluate_scenarios

pytestmark = pytest.mark.unit


def patient_frame(**overrides: float) -> pd.DataFrame:
    base = {'Pregnancies': 2, 'Glucose': 120, 'BloodPressure': 70,
            'SkinThickness': 25, 'Insulin': 100, 'BMI': 28.0,
            'DiabetesPedigreeFunction': 0.4, 'Age': 35}
    base.update(overrides)
    return pd.DataFrame([base], columns=list(DIABETES.features))


def heart_frame(**overrides: float) -> pd.DataFrame:
    base = {'Age': 50, 'Sex': 1, 'ChestPain': 4, 'RestingBP': 130,
            'Cholesterol': 230, 'FastingBS': 0, 'RestECG': 0,
            'MaxHeartRate': 150, 'ExerciseAngina': 0, 'STDepression': 1.0,
            'Slope': 2, 'MajorVessels': 0, 'Thallium': 3}
    base.update(overrides)
    return pd.DataFrame([base], columns=list(HEART.features))


# ---------- registry ----------

def test_registry_configs_are_consistent() -> None:
    for config in REGISTRY.values():
        form_cols = {f['col'] for f in config.form_spec}
        assert form_cols == set(config.features), config.key
        assert all(col in config.features for col, _ in config.strip_fields)
        (ax_x, _), (ax_y, _) = config.similar_axes
        assert ax_x in config.features and ax_y in config.features


# ---------- data ----------

def test_mark_missing_replaces_impossible_zeros_only() -> None:
    df = patient_frame(Glucose=0, Pregnancies=0)
    out = mark_missing(df, DIABETES)
    assert np.isnan(out.iloc[0]['Glucose'])
    assert out.iloc[0]['Pregnancies'] == 0          # zero pregnancies is real
    assert df.iloc[0]['Glucose'] == 0               # input frame not mutated


# ---------- risk / threshold ----------

def test_select_threshold_respects_recall_rule() -> None:
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    score = np.array([0.1, 0.2, 0.3, 0.6, 0.4, 0.5, 0.7, 0.9])
    thr = select_threshold(y, score, min_recall=0.75)
    pred = score >= thr
    recall = (pred & (y == 1)).sum() / y.sum()
    assert recall >= 0.75


def test_classify_tiers_ordered() -> None:
    thr = 0.30
    assert classify(0.05, thr).name == 'Low'
    assert classify(0.20, thr).name == 'Moderate'
    assert classify(0.45, thr).name == 'High'
    assert classify(0.90, thr).name == 'Very High'
    with pytest.raises(ValueError):
        classify(1.5, thr)


# ---------- drivers ----------

def test_drivers_rank_glucose_for_high_glucose_patient() -> None:
    typical = patient_frame().iloc[0]

    def fake_model(frame: pd.DataFrame) -> np.ndarray:
        return np.clip((frame['Glucose'].to_numpy() - 100) * 0.005, 0, 1)

    patient = patient_frame(Glucose=190)
    drivers = compute_drivers(fake_model, patient, typical)
    assert drivers[0].feature == 'Glucose'
    assert drivers[0].risk_delta > 0.3


# ---------- what-if: diabetes ----------

def test_diabetes_scenarios_only_applicable_and_never_mutate() -> None:
    patient = patient_frame(BMI=24.0, Glucose=100, Insulin=100)
    assert DIABETES.build_scenarios(patient) == []
    heavy = patient_frame(BMI=35.0, Glucose=180, Insulin=200)
    labels = [s.label for s in DIABETES.build_scenarios(heavy)]
    assert any('BMI -5' in lb for lb in labels)
    assert any('glucose' in lb.lower() for lb in labels)
    assert heavy.iloc[0]['BMI'] == 35.0


def test_evaluate_scenarios_reports_risk_drop() -> None:
    def fake_model(frame: pd.DataFrame) -> np.ndarray:
        return np.clip(frame['BMI'].to_numpy() / 100, 0, 1)

    heavy = patient_frame(BMI=40.0)
    results = evaluate_scenarios(fake_model, heavy, DIABETES.build_scenarios(heavy))
    bmi5 = next(r for r in results if 'BMI -5' in r.label)
    assert bmi5.risk_delta == pytest.approx(-0.05, abs=1e-6)


# ---------- what-if: heart ----------

def test_heart_scenarios_target_cholesterol_and_bp() -> None:
    healthy = heart_frame(Cholesterol=180, RestingBP=120)
    assert HEART.build_scenarios(healthy) == []
    risky = heart_frame(Cholesterol=280, RestingBP=150)
    labels = [s.label for s in HEART.build_scenarios(risky)]
    assert any('cholesterol' in lb.lower() for lb in labels)
    assert any('BP' in lb for lb in labels)


# ---------- recommendations ----------

def test_diabetes_recommendations_cite_patient_values() -> None:
    risky = patient_frame(Glucose=180, BMI=32.0, Age=50)
    recs = DIABETES.build_recommendations(risky, 0.7)
    text = ' '.join(r.title + r.reason for r in recs)
    assert 'impaired glucose tolerance' in text
    assert 'obese range' in text
    assert recs[0].title.startswith('Discuss')


def test_heart_recommendations_cover_guideline_ranges() -> None:
    risky = heart_frame(Cholesterol=250, RestingBP=145, ExerciseAngina=1,
                        FastingBS=1, Age=60)
    recs = HEART.build_recommendations(risky, 0.7)
    text = ' '.join(r.title + r.reason for r in recs)
    assert 'high range' in text                      # cholesterol >= 240
    assert 'stage-2' in text                         # BP >= 140
    assert 'angina' in text.lower()
    assert recs[0].title.startswith('Discuss')


def test_healthy_patients_get_maintenance() -> None:
    healthy_d = patient_frame(Glucose=95, BMI=22.0, Insulin=80, Age=25)
    healthy_h = heart_frame(Cholesterol=180, RestingBP=118, Age=30)
    for config, patient in ((DIABETES, healthy_d), (HEART, healthy_h)):
        recs = config.build_recommendations(patient, 0.05)
        assert len(recs) == 1
        assert 'Keep doing' in recs[0].title

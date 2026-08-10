"""Unit tests for the core layers (fast: tiny ensembles, synthetic data)."""
import numpy as np
import pandas as pd
import pytest

from edp.data import ALL_FEATURES, mark_missing
from edp.drivers import compute_drivers
from edp.recommend import build_recommendations
from edp.risk import classify, select_threshold
from edp.whatif import build_scenarios, evaluate_scenarios

pytestmark = pytest.mark.unit


def patient_frame(**overrides: float) -> pd.DataFrame:
    base = {'Pregnancies': 2, 'Glucose': 120, 'BloodPressure': 70,
            'SkinThickness': 25, 'Insulin': 100, 'BMI': 28.0,
            'DiabetesPedigreeFunction': 0.4, 'Age': 35}
    base.update(overrides)
    return pd.DataFrame([base], columns=list(ALL_FEATURES))


# ---------- data ----------

def test_mark_missing_replaces_impossible_zeros_only() -> None:
    df = patient_frame(Glucose=0, Pregnancies=0)
    out = mark_missing(df)
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
        # Risk is driven purely by glucose: 0.005 per unit above 100.
        return np.clip((frame['Glucose'].to_numpy() - 100) * 0.005, 0, 1)

    patient = patient_frame(Glucose=190)
    drivers = compute_drivers(fake_model, patient, typical)
    assert drivers[0].feature == 'Glucose'
    assert drivers[0].risk_delta > 0.3


# ---------- what-if ----------

def test_scenarios_only_applicable_and_never_mutate() -> None:
    patient = patient_frame(BMI=24.0, Glucose=100, Insulin=100)
    assert build_scenarios(patient) == []           # healthy: nothing to improve
    heavy = patient_frame(BMI=35.0, Glucose=180, Insulin=200)
    labels = [s.label for s in build_scenarios(heavy)]
    assert any('BMI -5' in lb for lb in labels)
    assert any('glucose' in lb.lower() for lb in labels)
    assert heavy.iloc[0]['BMI'] == 35.0             # untouched


def test_evaluate_scenarios_reports_risk_drop() -> None:
    def fake_model(frame: pd.DataFrame) -> np.ndarray:
        return np.clip(frame['BMI'].to_numpy() / 100, 0, 1)

    heavy = patient_frame(BMI=40.0)
    scenarios = build_scenarios(heavy)
    results = evaluate_scenarios(fake_model, heavy, scenarios)
    bmi5 = next(r for r in results if 'BMI -5' in r.label)
    assert bmi5.risk_delta == pytest.approx(-0.05, abs=1e-6)


# ---------- recommendations ----------

def test_recommendations_cite_patient_values() -> None:
    risky = patient_frame(Glucose=180, BMI=32.0, Age=50)
    recs = build_recommendations(risky, risk=0.7)
    text = ' '.join(r.title + r.reason for r in recs)
    assert 'impaired glucose tolerance' in text
    assert 'obese range' in text
    assert 'screening' in text.lower()
    assert recs[0].title.startswith('Discuss')      # high risk goes first


def test_recommendations_healthy_patient_gets_maintenance() -> None:
    healthy = patient_frame(Glucose=95, BMI=22.0, Insulin=80, Age=25)
    recs = build_recommendations(healthy, risk=0.05)
    assert len(recs) == 1
    assert 'Keep doing' in recs[0].title

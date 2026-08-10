"""Per-assessment cached computation - each patient is scored ONCE.

The 200-model pass, the risk drivers, and the what-if table are all cached
by (disease, patient values). Every tab reads the same cached result, so
switching tabs or rerunning costs nothing; only a genuinely new patient
triggers model work.
"""
import numpy as np
import pandas as pd
import streamlit as st

from edp.drivers import compute_drivers
from edp.whatif import evaluate_scenarios
from loader import load_art


def patient_key(patient: pd.DataFrame) -> tuple:
    """Hashable cache key for a patient row (NaN -> None)."""
    return tuple(None if pd.isna(v) else float(v) for v in patient.iloc[0])


def _frame(config, values: tuple) -> pd.DataFrame:
    row = [np.nan if v is None else v for v in values]
    return pd.DataFrame([row], columns=list(config.features))


@st.cache_data(show_spinner="Scoring with all 200 models...", max_entries=64)
def risk_distribution(disease_key: str, values: tuple) -> np.ndarray:
    """All 200 members' risk estimates for one patient - the headline pass."""
    art = load_art(disease_key)
    return art['ensemble'].predict_dist(_frame(art['config'], values))[:, 0]


@st.cache_data(show_spinner="Computing risk drivers...", max_entries=64)
def driver_rows(disease_key: str, values: tuple) -> list[dict]:
    """Median-substitution risk drivers, as plain dicts (cache-friendly)."""
    art = load_art(disease_key)
    patient = _frame(art['config'], values)
    drivers = compute_drivers(art['ensemble'].predict_mean, patient,
                              art['medians'])
    return [d._asdict() for d in drivers]


@st.cache_data(show_spinner="Simulating what-if scenarios...", max_entries=64)
def whatif_rows(disease_key: str, values: tuple) -> list[dict]:
    """Evaluated what-if scenarios, as plain dicts (cache-friendly)."""
    art = load_art(disease_key)
    patient = _frame(art['config'], values)
    scenarios = art['config'].build_scenarios(patient)
    results = evaluate_scenarios(art['ensemble'].predict_mean, patient,
                                 scenarios)
    return [r._asdict() for r in results]

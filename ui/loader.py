"""Loads trained artifacts once and caches them across reruns."""
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))  # so pickles resolve edp.* classes

from edp.data import load_clean  # noqa: E402

MODELS_DIR = PROJECT_ROOT / 'models'
DATASET = PROJECT_ROOT / 'datasets' / 'diabetes.csv'


@st.cache_resource(show_spinner="Loading trained models...")
def load_artifacts() -> dict:
    """Trained ensemble, similarity engine, metrics report, and the population."""
    missing = [p.name for p in (MODELS_DIR / 'ensemble.pkl',
                                MODELS_DIR / 'neighbors.pkl',
                                MODELS_DIR / 'metrics.json') if not p.exists()]
    if missing:
        st.error(f"Missing artifacts: {missing}. Run `python src/edp/train.py` first.")
        st.stop()
    X, y = load_clean(DATASET)
    report = json.loads((MODELS_DIR / 'metrics.json').read_text())
    return {
        'ensemble': joblib.load(MODELS_DIR / 'ensemble.pkl'),
        'similar': joblib.load(MODELS_DIR / 'neighbors.pkl'),
        'report': report,
        'population_X': X,
        'population_y': y,
        'medians': pd.Series(report['population_medians']),
    }

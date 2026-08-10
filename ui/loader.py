"""Loads trained artifacts lazily, one disease at a time, cached across reruns.

Lazy loading matters on the free hosting tier: the intake page renders
without touching any model file; a 36 MB ensemble is unpickled only when
its disease is actually assessed, and then kept in memory.
"""
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))  # so pickles resolve edp.* classes

from edp.data import load_clean          # noqa: E402
from edp.diseases import REGISTRY        # noqa: E402

MODELS_DIR = PROJECT_ROOT / 'models'


@st.cache_resource(show_spinner="Loading the trained model...")
def load_art(disease_key: str) -> dict:
    """One disease's trained ensemble, similarity engine, report, population."""
    config = REGISTRY[disease_key]
    out_dir = MODELS_DIR / disease_key
    missing = [p.name for p in (out_dir / 'ensemble.pkl',
                                out_dir / 'neighbors.pkl',
                                out_dir / 'metrics.json') if not p.exists()]
    if missing:
        st.error(f"Missing artifacts for {config.name}: {missing}. "
                 "Run `python src/edp/train.py` first.")
        st.stop()
    X, y = load_clean(config, PROJECT_ROOT)
    report = json.loads((out_dir / 'metrics.json').read_text())
    return {
        'config': config,
        'ensemble': joblib.load(out_dir / 'ensemble.pkl'),
        'similar': joblib.load(out_dir / 'neighbors.pkl'),
        'report': report,
        'population_X': X,
        'population_y': y,
        'medians': pd.Series(report['population_medians']),
    }

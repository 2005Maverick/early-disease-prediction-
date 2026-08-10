"""Loads trained artifacts for every registered disease, cached across reruns."""
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


@st.cache_resource(show_spinner="Loading trained models...")
def load_artifacts() -> dict[str, dict]:
    """Per-disease: trained ensemble, similarity engine, report, population."""
    arts: dict[str, dict] = {}
    for key, config in REGISTRY.items():
        out_dir = MODELS_DIR / key
        missing = [p.name for p in (out_dir / 'ensemble.pkl',
                                    out_dir / 'neighbors.pkl',
                                    out_dir / 'metrics.json') if not p.exists()]
        if missing:
            st.error(f"Missing artifacts for {config.name}: {missing}. "
                     "Run `python src/edp/train.py` first.")
            st.stop()
        X, y = load_clean(config, PROJECT_ROOT)
        report = json.loads((out_dir / 'metrics.json').read_text())
        arts[key] = {
            'config': config,
            'ensemble': joblib.load(out_dir / 'ensemble.pkl'),
            'similar': joblib.load(out_dir / 'neighbors.pkl'),
            'report': report,
            'population_X': X,
            'population_y': y,
            'medians': pd.Series(report['population_medians']),
        }
    return arts

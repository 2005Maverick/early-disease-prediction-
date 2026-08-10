"""Early Disease Prediction System - entry point.

Flow: choose disease -> intake form -> Run assessment -> report. Nothing is
predicted until the user asks; each patient is scored ONCE (cached) and all
report sections share that result.

Run:  .venv\\Scripts\\python.exe -m streamlit run ui\\main.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Early Disease Prediction System",
                   page_icon="🩺", layout="wide")

from theme import inject_css                       # noqa: E402
from components import intake_state, masthead, patient_strip  # noqa: E402
from loader import load_art                        # noqa: E402
from inputs import intake_form                     # noqa: E402
from compute import patient_key, risk_distribution  # noqa: E402
from edp.diseases import REGISTRY                  # noqa: E402
import tab_risk, tab_similar, tab_whatif, tab_plan, tab_lab  # noqa: E402

inject_css()

# Demo mode (?demo=diabetes|heart) preloads an example patient - used for
# documentation screenshots and quick presentations.
DEMO_PATIENTS = {
    'diabetes': [2, 190, 70, np.nan, 100, 40.0, 0.4, 55],
    'heart': [63, 1, 4, 145, 280, 0, 0, 120, 1, 2.5, 2, 1, 7],
}
demo_key = st.query_params.get('demo')

config, patient, submitted = intake_form(default_key=demo_key)
if submitted:
    st.session_state['assessed'] = {'key': config.key, 'patient': patient}
elif demo_key in DEMO_PATIENTS and 'assessed' not in st.session_state:
    demo_df = pd.DataFrame([DEMO_PATIENTS[demo_key]],
                           columns=list(REGISTRY[demo_key].features))
    st.session_state['assessed'] = {'key': demo_key, 'patient': demo_df}

masthead()

assessed = st.session_state.get('assessed')
if not assessed or assessed['key'] != config.key:
    if assessed and assessed['key'] != config.key:
        st.info(f"The intake is now set to **{config.name}** — fill the form "
                "and run the assessment to produce this report.")
    intake_state()
    st.stop()

patient = assessed['patient']
values = patient_key(patient)
art = load_art(config.key)
# The one 200-model pass for this patient; every tab reads from it.
art = {**art, 'values': values,
       'dist': risk_distribution(config.key, values)}
patient_strip(patient, config)

SECTIONS = {'findings': lambda: tab_risk.render(patient, art),
            'similar': lambda: tab_similar.render(patient, art),
            'whatif': lambda: tab_whatif.render(patient, art),
            'plan': lambda: tab_plan.render(patient, art),
            'lab': lambda: tab_lab.render(art)}

section = st.query_params.get('section')
if section in SECTIONS:  # single-section view for screenshots/presentations
    SECTIONS[section]()
else:
    tabs = st.tabs(["Findings", "Patients Like You", "What-If Simulator",
                    "Preventive Plan", "Data & Model Lab"])
    for tab, render in zip(tabs, SECTIONS.values()):
        with tab:
            render()

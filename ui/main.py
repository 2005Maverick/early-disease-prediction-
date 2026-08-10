"""Early Disease Prediction System - entry point.

Flow: intake form -> Run assessment -> report. Nothing is predicted until
the user asks; the report always names the patient it describes.

Run:  .venv\\Scripts\\python.exe -m streamlit run ui\\main.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

st.set_page_config(page_title="Early Disease Prediction System",
                   page_icon="🩺", layout="wide")

from theme import inject_css                       # noqa: E402
from components import intake_state, masthead, patient_strip  # noqa: E402
from loader import load_artifacts                  # noqa: E402
from inputs import intake_form                     # noqa: E402
import tab_risk, tab_similar, tab_whatif, tab_plan, tab_lab  # noqa: E402

inject_css()
art = load_artifacts()

patient, submitted = intake_form()
if submitted:
    st.session_state['patient'] = patient

masthead()

if 'patient' not in st.session_state:
    intake_state()
    st.stop()

patient = st.session_state['patient']
patient_strip(patient)

tabs = st.tabs(["Findings", "Patients Like You", "What-If Simulator",
                "Preventive Plan", "Data & Model Lab"])
with tabs[0]:
    tab_risk.render(patient, art)
with tabs[1]:
    tab_similar.render(patient, art)
with tabs[2]:
    tab_whatif.render(patient, art)
with tabs[3]:
    tab_plan.render(patient, art)
with tabs[4]:
    tab_lab.render(art)

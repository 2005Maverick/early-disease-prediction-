"""Intake form. A real form: nothing runs until 'Run assessment' is pressed.

Values marked unknown become NaN - the pipeline imputes the study median,
so the instrument works with incomplete labs.
"""
import numpy as np
import pandas as pd
import streamlit as st

from edp.data import ALL_FEATURES


def intake_form() -> tuple[pd.DataFrame | None, bool]:
    """Render the sidebar intake form; return (patient, submitted)."""
    with st.sidebar.form("intake", border=False):
        st.header("Patient intake")
        glucose = st.number_input("Glucose (2h OGTT, mg/dL)", 40, 300, 120)
        bmi = st.number_input("BMI", 15.0, 70.0, 30.0, step=0.1, format="%.1f")
        age = st.number_input("Age (years)", 18, 100, 33)
        blood_pressure = st.number_input("Blood pressure (diastolic, mm Hg)",
                                         30, 140, 70)
        pregnancies = st.number_input("Pregnancies", 0, 20, 2)
        pedigree = st.number_input("Family history score (pedigree)", 0.0, 2.5,
                                   0.4, step=0.01, format="%.2f",
                                   help="Higher = more relatives with diabetes")
        insulin = st.number_input("Insulin (2h serum, mu U/ml)", 10, 900, 100)
        insulin_unknown = st.checkbox("Insulin unknown")
        skin = st.number_input("Skin thickness (mm)", 5, 100, 25)
        skin_unknown = st.checkbox("Skin thickness unknown", value=True)
        st.caption("Unknown values are imputed with the study median.")
        submitted = st.form_submit_button("Run assessment", type="primary")

    if not submitted:
        return None, False
    row = {'Pregnancies': pregnancies, 'Glucose': glucose,
           'BloodPressure': blood_pressure,
           'SkinThickness': np.nan if skin_unknown else skin,
           'Insulin': np.nan if insulin_unknown else insulin,
           'BMI': bmi, 'DiabetesPedigreeFunction': pedigree, 'Age': age}
    return pd.DataFrame([row], columns=list(ALL_FEATURES)), True

"""Tab 4 - Preventive plan: rule-based actions citing the patient's own numbers."""
import pandas as pd
import streamlit as st

from components import plan_entry, section


def render(patient: pd.DataFrame, art: dict) -> None:
    risk = float(art['dist'].mean())
    section("Personalized preventive actions",
            "Deliberately rule-based, from published clinical reference ranges — "
            "every advice line traces to a guideline, not a statistical artifact.")
    for rec in art['config'].build_recommendations(patient, risk):
        plan_entry(rec.title, rec.reason, rec.action)
    st.caption("")
    st.warning("Educational project — not medical advice. Decisions belong "
               "with a healthcare professional.")

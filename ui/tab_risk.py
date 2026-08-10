"""Tab 1 - Risk Assessment: verdict, the full risk distribution, and personal
risk drivers."""
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from components import finding_block, section
from edp.drivers import compute_drivers
from edp.risk import classify
from theme import INK, MOSS, MUTED, OXBLOOD, styled

FRIENDLY = {'Pregnancies': 'Pregnancies', 'Glucose': 'Blood glucose',
            'BloodPressure': 'Blood pressure', 'SkinThickness': 'Skin thickness',
            'Insulin': 'Insulin', 'BMI': 'BMI',
            'DiabetesPedigreeFunction': 'Family history', 'Age': 'Age'}


def render(patient: pd.DataFrame, art: dict) -> None:
    ensemble = art['ensemble']
    threshold = art['report']['threshold']

    dist = ensemble.predict_dist(patient)[:, 0]
    mean_risk = float(dist.mean())
    lo, hi = float(np.percentile(dist, 5)), float(np.percentile(dist, 95))
    tier = classify(mean_risk, threshold)
    finding_block(tier.name, mean_risk, lo, hi, threshold)

    section("What all 200 models say",
            "Each model was trained on a different resample of the study. "
            "A narrow histogram means the models agree; a wide one means "
            "the system is honestly less certain.")
    hist_df = pd.DataFrame({'risk': dist * 100})
    chart = (
        alt.Chart(hist_df).mark_bar(opacity=0.92, color=OXBLOOD, cornerRadiusEnd=1)
        .encode(x=alt.X('risk:Q', bin=alt.Bin(step=2.5), title='Predicted risk (%)',
                        scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('count()', title='Number of models'))
        + alt.Chart(pd.DataFrame({'x': [mean_risk * 100]})).mark_rule(
            color=INK, size=2).encode(x='x:Q')
        + alt.Chart(pd.DataFrame({'x': [threshold * 100]})).mark_rule(
            color=MUTED, strokeDash=[6, 4], size=1.5).encode(x='x:Q')
    ).properties(height=250)
    st.altair_chart(styled(chart), use_container_width=True)
    st.caption("Ink line — this patient's score. Dashed line — alert threshold.")

    section("Personal risk drivers",
            "How much each factor adds to this patient's risk, measured by "
            "replacing it with the study's typical (median) value.")
    drivers = compute_drivers(ensemble.predict_mean, patient, art['medians'])
    drv_df = pd.DataFrame([
        {'Factor': FRIENDLY[d.feature], 'Adds to risk (%)': round(d.risk_delta * 100, 1)}
        for d in drivers if abs(d.risk_delta) >= 0.005
    ])
    if drv_df.empty:
        st.info("No single factor stands out - risk is spread across many small effects.")
        return
    bars = (
        alt.Chart(drv_df).mark_bar(cornerRadiusEnd=3)
        .encode(x=alt.X('Adds to risk (%):Q'),
                y=alt.Y('Factor:N', sort='-x', title=''),
                color=alt.condition(alt.datum['Adds to risk (%)'] > 0,
                                    alt.value(OXBLOOD), alt.value(MOSS)))
        .properties(height=42 + 32 * len(drv_df))
    )
    st.altair_chart(styled(bars), use_container_width=True)

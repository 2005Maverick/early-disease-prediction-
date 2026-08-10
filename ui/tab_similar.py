"""Tab 2 - Patients Like You: a second, model-free opinion from the 50 most
similar real patients in the study."""
import altair as alt
import pandas as pd
import streamlit as st

from components import section
from theme import INK, MOSS, OXBLOOD, POP_GREY, styled


def render(patient: pd.DataFrame, art: dict) -> None:
    view = art['similar'].query(patient)
    ens_risk = float(art['ensemble'].predict_mean(patient)[0])

    st.markdown(
        f"### Of the **{view.n_neighbors}** most similar patients, "
        f"**{view.n_diabetic}** developed diabetes — {view.risk * 100:.0f}%")
    c1, c2 = st.columns(2)
    c1.metric("Similar-patients risk", f"{view.risk * 100:.0f}%")
    c2.metric("Uncertainty Engine risk", f"{ens_risk * 100:.1f}%",
              help="The two numbers come from completely different methods.")
    agree = abs(view.risk - ens_risk) <= 0.15
    (st.success if agree else st.info)(
        "The two independent methods "
        + ("agree — that strengthens confidence in the result."
           if agree else
           "differ noticeably — treat the result with extra care. This happens "
           "for unusual patients, exactly when caution is right."))

    section("Where this patient sits",
            "Blood glucose against BMI. Grey — the whole study. Colored — the "
            "50 most similar patients. The diamond is this patient.")
    pop = art['population_X'].assign(Outcome=art['population_y'].values)
    pop_pts = pop[['Glucose', 'BMI']].assign(group='All patients')
    nb = view.neighbor_rows
    nb_pts = nb[['Glucose', 'BMI']].assign(
        group=nb['Outcome'].map({1: 'Similar — developed diabetes',
                                 0: 'Similar — stayed healthy'}))
    me = patient[['Glucose', 'BMI']].assign(group='This patient')
    plot_df = pd.concat([pop_pts, nb_pts, me], ignore_index=True).dropna()

    color_scale = alt.Scale(
        domain=['All patients', 'Similar — stayed healthy',
                'Similar — developed diabetes', 'This patient'],
        range=[POP_GREY, MOSS, OXBLOOD, INK])
    base = alt.Chart(plot_df).encode(
        x=alt.X('Glucose:Q', title='Blood glucose (mg/dL)'),
        y=alt.Y('BMI:Q', title='BMI'),
        color=alt.Color('group:N', scale=color_scale, title=''))
    layers = (
        base.transform_filter(alt.datum.group == 'All patients').mark_circle(size=26, opacity=0.5)
        + base.transform_filter((alt.datum.group != 'All patients')
                                & (alt.datum.group != 'This patient')).mark_circle(size=75, opacity=0.9)
        + base.transform_filter(alt.datum.group == 'This patient').mark_point(
            shape='diamond', size=380, filled=True, stroke='#faf6ef', strokeWidth=1.5)
    ).properties(height=390)
    st.altair_chart(styled(layers), use_container_width=True)

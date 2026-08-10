"""Tab 5 - Data & Model Lab: the honesty exhibit.

Everything a skeptical examiner would ask for: the hidden-missing-data fix,
out-of-fold metrics, the model comparison, the threshold rule, and proof the
probabilities are calibrated.
"""
import altair as alt
import pandas as pd
import streamlit as st

from components import section
from theme import MUTED, OXBLOOD, styled


def render(art: dict) -> None:
    report = art['report']
    st.caption(f"Model: {report['disease']} — trained on {report['trained_on']}.")

    section("The dataset's hidden missing values",
            "Zeros in these columns are physiologically impossible — "
            "undocumented missing values. We mark them missing and impute the "
            "study median inside each training fold.")
    st.dataframe(pd.DataFrame(report['missingness']),
                 use_container_width=True, hide_index=True)

    section("Honest performance",
            f"Every number below was measured on patients the model never saw "
            f"during training ({report['cv_folds']}-fold out-of-fold "
            f"cross-validation).")
    dep = report['deployed_metrics']
    cols = st.columns(5)
    for col, (name, key) in zip(cols, [('Accuracy', 'accuracy'), ('Precision', 'precision'),
                                       ('Recall', 'recall'), ('F1', 'f1'),
                                       ('ROC AUC', 'roc_auc')]):
        col.metric(name, f"{dep[key]}%")

    section("Model comparison",
            "Same folds, same threshold, no favorites.")
    comp = pd.DataFrame(report['model_comparison']).T.reset_index(names='Model')
    st.dataframe(comp, use_container_width=True, hide_index=True)

    section("The alert threshold is a stated rule",
            "Missing a diabetic costs more than a false alarm — that asymmetry "
            "is the whole justification.")
    st.info(f"Rule: never miss more than {(1 - report['min_recall_rule']) * 100:.0f}% "
            f"of true diabetics (recall ≥ {report['min_recall_rule'] * 100:.0f}%), then "
            f"maximize precision. Result: alert at "
            f"**{report['threshold'] * 100:.1f}%** risk.")

    section("Are the probabilities honest?",
            "Patients are grouped by predicted risk; within each group the "
            "prediction should match the share who actually developed diabetes. "
            "Points near the diagonal — honest probabilities.")
    cal = pd.DataFrame(report['calibration'])
    diag = pd.DataFrame({'predicted': [0, 100], 'observed': [0, 100]})
    chart = (
        alt.Chart(diag).mark_line(color=MUTED, strokeDash=[6, 4]).encode(
            x=alt.X('predicted:Q', title='Predicted risk (%)',
                    scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('observed:Q', title='Observed diabetes rate (%)',
                    scale=alt.Scale(domain=[0, 100])))
        + alt.Chart(cal).mark_circle(size=130, color=OXBLOOD).encode(
            x='predicted:Q', y='observed:Q',
            tooltip=['predicted', 'observed', 'patients'])
        + alt.Chart(cal).mark_line(color=OXBLOOD, opacity=.6).encode(
            x='predicted:Q', y='observed:Q')
    ).properties(height=330)
    st.altair_chart(styled(chart), use_container_width=True)

    section("Architecture in one breath", "")
    st.markdown(
        "- **Data layer** — impossible zeros → missing → imputed per fold (no leakage)\n"
        "- **Uncertainty Engine** — 200 models on bootstrap resamples → a risk "
        "*distribution*, not just a number\n"
        "- **Patients Like You** — an independent, model-free second opinion\n"
        "- **Decision layer** — threshold from a stated recall rule\n"
        "- **Explanation layer** — median-substitution risk drivers + what-if simulator\n"
        "- **Prevention layer** — clinical-guideline rules citing the patient's own values")

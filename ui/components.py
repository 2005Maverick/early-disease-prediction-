"""Lab Report shared components: masthead, intake state, patient strip,
finding block, plan entries."""
import pandas as pd
import streamlit as st

from theme import MUTED, TIER_COLORS

_SEAL = """<svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="vertical-align:-5px;margin-right:10px">
<circle cx="15" cy="15" r="13.5" stroke="#8e2f22" stroke-width="1.6"/>
<path d="M6 16h4l2.5-6.5 4 11 2.5-6h5" stroke="#1c1a17" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def masthead() -> None:
    st.markdown(
        f"""<div class="edp-masthead">
        <h1>{_SEAL}Early Disease Prediction — Assessment Report</h1>
        <div class="dek">Disease risk before symptoms — diabetes and heart disease.
        Two hundred models vote; the fifty most similar real patients give an
        independent second opinion.</div>
        </div>""",
        unsafe_allow_html=True)


def intake_state() -> None:
    """First-run state: explain the instrument; nothing is predicted yet."""
    st.markdown(
        """<div class="edp-intake">
        <p style="font-size:1.1rem">No assessment has been run yet.
        This instrument produces a risk report only when you ask it to.</p>
        <div class="step"><span class="n">1</span><span>
          <span class="t">Choose a disease and enter the patient's data</span><br>
          <span class="d">Pick diabetes or heart disease, then fill the intake
          form on the left. Values you don't know can be marked unknown — the
          model imputes the study median.</span></span></div>
        <div class="step"><span class="n">2</span><span>
          <span class="t">Run the assessment</span><br>
          <span class="d">All 200 models score the patient; the 50 most similar
          real patients are found for a second opinion.</span></span></div>
        <div class="step"><span class="n">3</span><span>
          <span class="t">Read the report</span><br>
          <span class="d">Risk with uncertainty, what drives it, what would
          change it, and a preventive plan — each in its own section.</span></span></div>
        </div>""",
        unsafe_allow_html=True)


def patient_strip(patient: pd.DataFrame, config) -> None:
    """Who this report is about - always visible above the findings."""
    r = patient.iloc[0]

    def fmt(v):
        return 'unknown' if pd.isna(v) else f'{v:g}'

    cells = ''.join(
        f'<span><span class="k">{label}</span> <b>{fmt(r[col])}</b></span>'
        for col, label in config.strip_fields)
    st.markdown(
        f'<div class="edp-strip"><span><span class="k">Assessment</span> '
        f'<b>{config.name}</b></span>{cells}</div>',
        unsafe_allow_html=True)
    st.caption("Edit the intake form and run the assessment again to update this report.")


def finding_block(tier_name: str, mean_risk: float, lo: float, hi: float,
                  threshold: float) -> None:
    """The headline finding - the report's one animated moment."""
    color = TIER_COLORS.get(tier_name, MUTED)
    above = mean_risk >= threshold
    line = ("Above the alert threshold — early screening is recommended."
            if above else "Below the alert threshold.")
    st.markdown(
        f"""<div class="edp-finding" style="background:
        linear-gradient(105deg, color-mix(in srgb, {color} 7%, #fffdf7), #fffdf7 55%)">
        <span class="tier" style="color:{color}">{tier_name} risk</span>
        <span class="num" style="font-size:1.5rem">&ensp;{mean_risk * 100:.1f}%</span><br>
        <span class="sub">90% confidence band
        <span class="num">{lo * 100:.0f}–{hi * 100:.0f}%</span>
        &middot; alert threshold <span class="num">{threshold * 100:.0f}%</span>
        &middot; {line}</span>
        </div>""",
        unsafe_allow_html=True)


def plan_entry(title: str, reason: str, action: str) -> None:
    st.markdown(
        f"""<div class="edp-plan">
        <div class="t">{title}</div>
        <div class="why">{reason}</div>
        <div class="act">{action}</div>
        </div>""",
        unsafe_allow_html=True)


def section(title: str, caption: str) -> None:
    st.markdown(f"#### {title}")
    if caption:
        st.caption(caption)

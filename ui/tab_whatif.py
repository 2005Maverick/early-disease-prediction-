"""Tab 3 - What-If simulator: what specific changes are worth in risk points."""
import altair as alt
import pandas as pd
import streamlit as st

from components import section
from compute import whatif_rows
from theme import MOSS, OXBLOOD, styled


def render(patient: pd.DataFrame, art: dict) -> None:
    base_risk = float(art['dist'].mean())
    results = whatif_rows(art['config'].key, art['values'])

    section("If this patient made one change",
            "Each row re-runs all 200 models with one value changed. "
            "Everything else stays the same.")
    if not results:
        st.success("All modifiable values are already in healthy ranges — "
                   "no meaningful what-if scenarios for this patient.")
        return

    df = pd.DataFrame([
        {'Change': r['label'],
         'New risk (%)': round(r['new_risk'] * 100, 1),
         'Risk change (points)': round(r['risk_delta'] * 100, 1)}
        for r in results
    ]).sort_values('Risk change (points)')

    chart = (
        alt.Chart(df).mark_bar(cornerRadiusEnd=3)
        .encode(x=alt.X('Risk change (points):Q',
                        title='Risk change (percentage points)'),
                y=alt.Y('Change:N', sort='x', title=''),
                color=alt.condition(alt.datum['Risk change (points)'] < 0,
                                    alt.value(MOSS), alt.value(OXBLOOD)))
        .properties(height=62 + 40 * len(df))
    )
    st.altair_chart(styled(chart), use_container_width=True)
    st.dataframe(
        df.assign(**{'Current risk (%)': round(base_risk * 100, 1)})
          [['Change', 'Current risk (%)', 'New risk (%)', 'Risk change (points)']],
        use_container_width=True, hide_index=True)
    best = df.iloc[0]
    if best['Risk change (points)'] < 0:
        st.info(f"Biggest single win: **{best['Change']}** — risk falls from "
                f"{base_risk * 100:.1f}% to {best['New risk (%)']}%.")

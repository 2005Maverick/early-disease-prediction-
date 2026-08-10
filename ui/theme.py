"""The Lab Report visual world: tokens, global CSS, and the journal chart theme.

Direction: a printed medical journal turned interactive. Warm paper ground,
ink text, one oxblood accent that owns all risk semantics, deep moss green
for health. Display: Bricolage Grotesque. Body: Newsreader (text serif with
optical sizing). Measured values only: Spline Sans Mono.
"""
import altair as alt
import streamlit as st

# ---- tokens ----------------------------------------------------------------
PAPER = '#faf6ef'        # app ground
PANEL = '#f1ebdf'        # sidebar / raised panels
CARD = '#fffdf7'         # report blocks
LINE = '#d9cfbc'         # hairlines
INK = '#1c1a17'
MUTED = '#6b6156'        # warm brown-gray secondary text (5.6:1 on paper)
OXBLOOD = '#8e2f22'      # risk accent
BRICK = '#b3471f'        # high tier
OCHRE = '#9a6519'        # caution (4.6:1 on paper)
MOSS = '#3a6b35'         # health
POP_GREY = '#b9b0a2'     # population marks on charts

TIER_COLORS = {'Low': MOSS, 'Moderate': OCHRE, 'High': BRICK,
               'Very High': OXBLOOD}

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Spline+Sans+Mono:wght@400;500&display=swap');

:root {{
  --paper: {PAPER}; --panel: {PANEL}; --card: {CARD}; --line: {LINE};
  --ink: {INK}; --muted: {MUTED}; --oxblood: {OXBLOOD};
}}

html, body, .stApp, [class*="css"] {{
  font-family: 'Newsreader', Georgia, serif;
  color: var(--ink);
  font-size: 1.02rem;
}}
.stApp {{ background: var(--paper); }}

h1, h2, h3, h4 {{
  font-family: 'Bricolage Grotesque', 'Newsreader', sans-serif !important;
  letter-spacing: -0.015em;
  color: var(--ink);
}}
h3, h4 {{ margin-top: 1.7rem !important; margin-bottom: .45rem !important; }}

[data-testid="stCaptionContainer"], .stCaption, small {{
  color: var(--muted) !important;
  font-family: 'Newsreader', serif;
}}

/* Sidebar: the intake form */
[data-testid="stSidebar"] {{
  background: var(--panel);
  border-right: 1px solid var(--line);
}}
[data-testid="stSidebar"] h2 {{ font-size: 1.15rem; }}
[data-testid="stSidebar"] label {{
  color: var(--ink) !important;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: .82rem;
}}
[data-testid="stSidebar"] input {{ font-family: 'Spline Sans Mono', monospace; }}

[data-testid="stNumberInput"] > div {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 4px;
}}
[data-testid="stNumberInput"] input:focus {{
  outline: 2px solid {OXBLOOD}; outline-offset: -1px;
}}

/* The one primary action */
[data-testid="stSidebar"] button[kind="primaryFormSubmit"],
[data-testid="stSidebar"] button[kind="secondaryFormSubmit"] {{
  background: {OXBLOOD};
  color: {PAPER};
  border: none; border-radius: 4px;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 600; font-size: 1rem;
  padding: .55rem 1rem; width: 100%;
  box-shadow: 0 2px 8px rgba(60, 24, 16, .25);
}}
[data-testid="stSidebar"] button[kind="primaryFormSubmit"]:hover {{
  background: #7a271c;
}}

/* Tabs as report section rail */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  gap: 2px; border-bottom: 2px solid var(--ink);
}}
[data-testid="stTabs"] button[data-baseweb="tab"] {{
  background: transparent; color: var(--muted);
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 600; font-size: .92rem;
  padding: 9px 16px;
}}
[data-testid="stTabs"] button[data-baseweb="tab"]:hover {{ color: var(--ink); }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: {OXBLOOD}; }}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
  background: {OXBLOOD}; height: 3px;
}}

/* Metrics as report figures */
[data-testid="stMetric"] {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 14px 16px 10px;
  box-shadow: 0 1px 3px rgba(60, 48, 30, .08);
}}
[data-testid="stMetricLabel"] p {{
  color: var(--muted) !important;
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: .74rem !important;
  text-transform: uppercase; letter-spacing: .07em;
}}
[data-testid="stMetricValue"] {{
  font-family: 'Spline Sans Mono', monospace;
  font-weight: 500; font-size: 1.8rem !important;
}}

[data-testid="stAlert"] {{
  border-radius: 6px;
  border: 1px solid var(--line);
  font-family: 'Newsreader', serif;
}}
[data-testid="stDataFrame"] {{
  border: 1px solid var(--line); border-radius: 6px;
}}

/* Masthead */
.edp-masthead {{ border-bottom: 3px double var(--ink); padding: 6px 0 14px; margin-bottom: 4px; }}
.edp-masthead h1 {{
  font-size: clamp(1.6rem, 4.5vw, 2.5rem);
  font-weight: 700; margin: 0;
}}
.edp-masthead .dek {{
  color: var(--muted); font-size: 1.02rem; font-style: italic;
  max-width: 66ch; margin-top: 2px;
}}

/* Patient summary strip */
.edp-strip {{
  display: flex; flex-wrap: wrap; gap: 6px 22px;
  background: var(--panel);
  border: 1px solid var(--line); border-radius: 6px;
  padding: 10px 16px; margin: 10px 0 4px;
  font-family: 'Spline Sans Mono', monospace; font-size: .86rem;
}}
.edp-strip b {{ font-family: 'Bricolage Grotesque', sans-serif; }}
.edp-strip .k {{ color: var(--muted); }}

/* Finding block: the one authored motion moment */
@keyframes finding-in {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.edp-finding {{
  animation: finding-in .5s cubic-bezier(.16, 1, .3, 1);
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 18px 22px;
  margin-top: 12px;
  box-shadow: 0 2px 10px rgba(60, 48, 30, .10);
}}
.edp-finding .tier {{
  font-family: 'Bricolage Grotesque', sans-serif;
  font-weight: 700; font-size: 1.5rem;
}}
.edp-finding .num {{ font-family: 'Spline Sans Mono', monospace; font-weight: 500; }}
.edp-finding .sub {{ color: var(--muted); font-size: .95rem; }}

/* Intake empty state */
.edp-intake {{ max-width: 62ch; }}
.edp-intake .step {{
  border-top: 1px solid var(--line);
  padding: 12px 0; display: flex; gap: 14px; align-items: baseline;
}}
.edp-intake .n {{
  font-family: 'Spline Sans Mono', monospace;
  color: {OXBLOOD}; font-size: .9rem; min-width: 1.4em;
}}
.edp-intake .t {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 600; }}
.edp-intake .d {{ color: var(--muted); font-size: .95rem; }}

/* Plan entries */
.edp-plan {{ border-top: 1px solid var(--line); padding: 13px 2px 15px; }}
.edp-plan:last-of-type {{ border-bottom: 1px solid var(--line); }}
.edp-plan .t {{ font-family: 'Bricolage Grotesque', sans-serif; font-weight: 600;
               font-size: 1.02rem; margin-bottom: 2px; }}
.edp-plan .why {{ color: var(--muted); font-size: .92rem; }}
.edp-plan .act {{ font-size: .97rem; margin-top: 4px; }}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def styled(chart: alt.LayerChart | alt.Chart) -> alt.LayerChart | alt.Chart:
    """Journal-figure chart theme: ink axes on paper, hairline grid."""
    return (chart
            .configure(background='transparent')
            .configure_view(stroke=None)
            .configure_axis(labelColor=MUTED, titleColor=MUTED,
                            gridColor='rgba(120, 104, 80, .16)',
                            domainColor=INK, tickColor=INK,
                            labelFont='Newsreader', titleFont='Bricolage Grotesque')
            .configure_legend(labelColor=INK, titleColor=MUTED,
                              labelFont='Newsreader'))

"""Intake: disease selector + a config-driven form.

The selector lives OUTSIDE the form (changing it redraws the fields);
the fields live INSIDE a form, so nothing runs until 'Run assessment'.
Unknown values become NaN - the pipeline imputes the study median.
"""
import numpy as np
import pandas as pd
import streamlit as st

from edp.diseases import REGISTRY
from edp.diseases.base import DiseaseConfig


def _render_field(spec: dict) -> float:
    kind = spec['kind']
    if kind in ('number', 'number_unknown'):
        kwargs = {k: spec[k] for k in ('step', 'format', 'help') if k in spec}
        value = st.number_input(spec['label'], spec['min'], spec['max'],
                                spec['default'], **kwargs)
        if kind == 'number_unknown':
            unknown = st.checkbox(f"{spec['label'].split(' (')[0]} unknown",
                                  value=spec.get('unknown_default', False),
                                  key=f"unk_{spec['col']}")
            return np.nan if unknown else value
        return value
    if kind in ('select', 'select_unknown'):
        labels = [lb for lb, _ in spec['options']]
        values = [v for _, v in spec['options']]
        if kind == 'select_unknown':
            labels.append('Unknown')
            values.append(np.nan)
        choice = st.selectbox(spec['label'], labels,
                              index=spec.get('default_index', 0),
                              key=f"sel_{spec['col']}")
        return values[labels.index(choice)]
    if kind == 'flag':
        return 1 if st.checkbox(spec['label'], key=f"flag_{spec['col']}") else 0
    raise ValueError(f"Unknown form field kind: {kind}")


def intake_form(default_key: str | None = None
                ) -> tuple[DiseaseConfig, pd.DataFrame | None, bool]:
    """Render the sidebar intake; return (config, patient, submitted)."""
    names = {c.name: c for c in REGISTRY.values()}
    keys = [c.key for c in names.values()]
    default_index = keys.index(default_key) if default_key in keys else 0
    with st.sidebar:
        st.header("Patient intake")
        chosen = st.radio("Assessment for", list(names), index=default_index,
                          horizontal=True)
        config = names[chosen]
        with st.form(f"intake_{config.key}", border=False):
            values: dict[str, float] = {}
            for spec in config.form_spec:
                values[spec['col']] = _render_field(spec)
            st.caption("Unknown values are imputed with the study median.")
            submitted = st.form_submit_button("Run assessment", type="primary")
    if not submitted:
        return config, None, False
    patient = pd.DataFrame([values], columns=list(config.features))
    return config, patient, True

"""Session state: form defaults, presets and navigation. Values unchanged."""

import streamlit as st

from .config import DEFAULT_PAGE

FORM_DEFAULTS = {
    "g1": 10, "g2": 10, "absences": 5, "failures": 0,
    "studytime": "2–5 hours", "schoolsup": "no", "famsup": "yes",
    "internet": "yes", "higher": "yes", "activities": "yes", "paid": "no",
}

PRESETS = {
    "high_risk": {
        "g1": 8, "g2": 7, "absences": 14, "failures": 2,
        "studytime": "Less than 2 hours", "schoolsup": "no", "famsup": "no",
        "internet": "yes", "higher": "no", "activities": "no", "paid": "no",
    },
    "low_risk": {
        "g1": 16, "g2": 17, "absences": 1, "failures": 0,
        "studytime": "5–10 hours", "schoolsup": "no", "famsup": "yes",
        "internet": "yes", "higher": "yes", "activities": "yes", "paid": "yes",
    },
    "reset": dict(FORM_DEFAULTS),
}


def init_session_state() -> None:
    for key, val in FORM_DEFAULTS.items():
        st.session_state.setdefault(key, val)
    st.session_state.setdefault("page", DEFAULT_PAGE)
    st.session_state.setdefault("assessment", None)


def apply_preset(preset_type: str) -> None:
    values = PRESETS.get(preset_type)
    if values:
        st.session_state.update(values)
    # A preset changes the inputs, so the previous result no longer describes them.
    st.session_state["assessment"] = None


def goto(page: str) -> None:
    st.session_state["page"] = page

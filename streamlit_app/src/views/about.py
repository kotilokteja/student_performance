"""About view."""

import streamlit as st

from ..components import back_button, page_header
from ..config import RISK_THRESHOLD_G3, FEATURES
from ..data import get_deployed_model_name


def render(ctx):
    ds, ev = ctx["ds"], ctx["eval"]
    deployed = get_deployed_model_name()

    back_button(key="back_about")
    page_header(
        "Project Overview",
        "About the System",
        "How the early-warning system is built, what it predicts and where its "
        "limits are.",
        icon="book",
    )

    sections = [
        ("01", "The Problem",
         "Institutions need data-driven ways to identify academic difficulty before final "
         "outcomes are locked in, so support can be proactive rather than reactive."),
        ("02", "The Solution",
         "A classification model combining academic history, attendance and contextual "
         "support signals to flag high-risk students instantly."),
        ("03", "Dataset",
         f"Trained on the UCI Student Performance dataset (Portuguese course), containing "
         f"{ds['total']} student records across {ds['n_columns']} attributes, of which "
         f"{len(FEATURES)} are used as model features."),
        ("04", "Risk Definition",
         f"Students with a final grade (G3) of {RISK_THRESHOLD_G3} or below are classified "
         f"as At Risk (1). Students scoring {RISK_THRESHOLD_G3 + 1} or above are Not At Risk (0)."),
        ("05", "Selected Model",
         f"{deployed} was selected for its interpretability, achieving "
         f"{ev['accuracy'] * 100:.1f}% accuracy and {ev['recall'] * 100:.1f}% recall on the "
         f"at-risk class across a held-out test set of {ev['test_size']} students."),
        ("06", "Intended Use",
         "The output is a screening signal to prioritise human review, not an automated "
         "decision about any individual student."),
    ]

    body = "".join(
        f'<div class="ag-about"><div class="ag-about-num">{num}</div>'
        f'<div><div class="ag-about-title">{title}</div>'
        f'<div class="ag-about-text">{text}</div></div></div>'
        for num, title, text in sections
    )
    with st.container(border=True):
        st.markdown(f'<div style="padding:4px 20px">{body}</div>', unsafe_allow_html=True)

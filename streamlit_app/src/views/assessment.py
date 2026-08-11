"""Risk Assessment view. Prediction logic is byte-for-byte the original."""

import io

import pandas as pd
import streamlit as st

from ..components import back_button, page_header, section, step_label
from ..config import (
    STUDY_TIME_OPTIONS, STUDY_TIME_TO_CODE, YES_NO_LABELS, YES_NO_OPTIONS,
)
from ..state import apply_preset
from ..theme import ICONS


def _yn(value: str) -> str:
    return YES_NO_LABELS.get(value, value)


def _risk_band(probability: float):
    """Presentation-only banding of the model's existing probability."""
    if probability < 0.35:
        return "Low", "safe"
    if probability < 0.65:
        return "Moderate", "warn"
    return "High", "risk"


def _empty_state():
    st.markdown(
        f"""
<div class="ag-empty">
  {ICONS['file']}
  <div class="ag-empty-title">Ready for assessment</div>
  <div class="ag-empty-text">Complete the student profile and run the model to generate a risk prediction.</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _result_panel(result):
    is_risk = result["prediction"] == 1
    probability = result["probability"]
    band, _tone = _risk_band(probability)
    variant = "risk" if is_risk else "safe"
    label = "AT RISK" if is_risk else "NOT AT RISK"
    icon = ICONS["alert"] if is_risk else ICONS["check"]

    st.markdown(
        f"""
<div class="ag-result ag-result--{variant}">
  <div class="ag-result-eyebrow">Assessment Result</div>
  <div class="ag-result-status">{icon}{label}</div>
  <div class="ag-result-figure">{probability * 100:.1f}%</div>
  <div class="ag-result-caption">
    Probability of academic risk
    <span class="ag-tip" data-tip="Model-estimated probability that the student belongs to the At Risk class.">i</span>
  </div>
  <div class="ag-meter" role="img" aria-label="Risk probability {probability * 100:.1f} percent">
    <div class="ag-meter-fill" style="width:{probability * 100:.1f}%"></div>
  </div>
  <div class="ag-meter-scale"><span>0%</span><span>50%</span><span>100%</span></div>
  <div class="ag-result-grid">
    <div class="ag-result-cell">
      <div class="ag-result-cell-label">Risk level</div>
      <div class="ag-result-cell-value">{band}</div>
    </div>
    <div class="ag-result-cell">
      <div class="ag-result-cell-label">Predicted class</div>
      <div class="ag-result-cell-value">{result['prediction']} &middot; {label.title()}</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def _interventions(result):
    inputs = result["inputs"]
    suggestions = []
    if inputs["G1"] < 10 or inputs["G2"] < 10:
        suggestions.append(("Priority", "warn", "Review low-performing subjects; arrange immediate tutoring."))
    if inputs["absences"] > 5:
        suggestions.append(("Warning", "warn", "Monitor attendance; investigate absence patterns with family."))
    if inputs["studytime"] <= 2:
        suggestions.append(("Action", "primary", "Build a structured weekly study schedule with the student."))
    if inputs["failures"] > 0:
        suggestions.append(("Priority", "warn", "Provide focused support for previously failed subjects."))
    if not suggestions:
        suggestions.append(("Clear", "safe", "Continue routine monitoring. No immediate intervention required."))

    section("Intervention Strategy", "Generated from the values submitted for this student.")
    rows = "".join(
        f'<div class="ag-insight"><span class="ag-badge ag-badge--{tone}">{tag}</span>'
        f'<div class="ag-insight-text" style="margin-top:2px">{text}</div></div>'
        for tag, tone, text in suggestions
    )
    with st.container(border=True):
        st.markdown(f'<div style="padding:4px 16px">{rows}</div>', unsafe_allow_html=True)


def render(ctx):
    model = ctx["model"]

    page_header(
        "Student Assessment",
        "Risk Assessment",
        "Enter a student profile to estimate the probability of academic risk "
        "before final grades are recorded.",
        icon="clipboard",
    )

    nav, p1, p2, p3 = st.columns([1.3, 1.25, 1.25, 0.9], gap="small")
    with nav:
        back_button(key="back_assessment")
    with p1:
        st.button("High-risk profile", on_click=apply_preset, args=("high_risk",),
                  use_container_width=True, key="preset_high")
    with p2:
        st.button("Low-risk profile", on_click=apply_preset, args=("low_risk",),
                  use_container_width=True, key="preset_low")
    with p3:
        st.button("Reset", on_click=apply_preset, args=("reset",),
                  use_container_width=True, key="preset_reset")

    left, right = st.columns([1.25, 1], gap="large")

    with left:
        with st.container(border=True):
            pad = st.container()
            with pad:
                st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
                step_label("01", "Academic Performance")
                a, b = st.columns(2, gap="medium")
                with a:
                    g1 = st.number_input("First period grade (G1)", 0, 20, key="g1",
                                         help="Grade scale from 0 to 20.")
                    absences = st.number_input("Absences", 0, 100, key="absences",
                                               help="Total classes missed.")
                with b:
                    g2 = st.number_input("Second period grade (G2)", 0, 20, key="g2",
                                         help="Grade scale from 0 to 20.")
                    failures = st.number_input("Previous failures", 0, 4, key="failures",
                                               help="Number of previously failed classes (max 4).")

                st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
                step_label("02", "Student Engagement")
                c, d = st.columns(2, gap="medium")
                with c:
                    # Human-readable band shown; the model receives 1–4 unchanged.
                    study_label = st.selectbox(
                        "Weekly study time", STUDY_TIME_OPTIONS, key="studytime",
                        help="Estimated hours spent studying outside class each week.",
                    )
                    activities = st.selectbox("Extracurricular activities", YES_NO_OPTIONS,
                                              key="activities", format_func=_yn)
                with d:
                    higher = st.selectbox("Plans higher education", YES_NO_OPTIONS,
                                          key="higher", format_func=_yn)
                    paid = st.selectbox("Extra paid classes", YES_NO_OPTIONS,
                                        key="paid", format_func=_yn)
                studytime_val = STUDY_TIME_TO_CODE[study_label]

                st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
                step_label("03", "Support & Environment")
                e, f = st.columns(2, gap="medium")
                with e:
                    schoolsup = st.selectbox("Extra school support", YES_NO_OPTIONS,
                                             key="schoolsup", format_func=_yn)
                    internet = st.selectbox("Internet access at home", YES_NO_OPTIONS,
                                            key="internet", format_func=_yn)
                with f:
                    famsup = st.selectbox("Family educational support", YES_NO_OPTIONS,
                                          key="famsup", format_func=_yn)

                st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)
                assess = st.button("Generate assessment", type="primary",
                                   use_container_width=True, key="run_assessment")
                st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # Prediction — identical to the original implementation.
    # ------------------------------------------------------------------
    if assess:
        student_data = {
            "absences": absences, "studytime": studytime_val, "failures": failures,
            "G1": g1, "G2": g2, "schoolsup": schoolsup, "famsup": famsup,
            "higher": higher, "internet": internet, "activities": activities, "paid": paid,
        }
        student_df = pd.DataFrame([student_data])
        prediction = int(model.predict(student_df)[0])
        probability = float(model.predict_proba(student_df)[0][1])

        st.session_state["assessment"] = {
            "inputs": student_data,
            "prediction": prediction,
            "probability": probability,
        }

    result = st.session_state.get("assessment")

    with right:
        if not result:
            _empty_state()
        else:
            _result_panel(result)

    if result:
        _interventions(result)

        export_df = pd.DataFrame([result["inputs"]])
        export_df["Risk_Probability"] = f'{result["probability"] * 100:.1f}%'
        export_df["Prediction"] = "AT RISK" if result["prediction"] == 1 else "NOT AT RISK"
        csv_buffer = io.StringIO()
        export_df.to_csv(csv_buffer, index=False)
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.download_button(
            label="Download assessment report (CSV)",
            data=csv_buffer.getvalue(),
            file_name="student_risk_assessment.csv",
            mime="text/csv",
            use_container_width=True,
        )

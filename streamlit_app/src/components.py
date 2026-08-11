"""Reusable presentational components. No business logic lives here."""

import streamlit as st

from .theme import ICONS


def _tip(text: str) -> str:
    if not text:
        return ""
    safe = text.replace('"', "&quot;")
    return f'<span class="ag-tip" data-tip="{safe}">i</span>'


def page_header(eyebrow: str, title: str, lede: str = "", icon: str = "grid") -> None:
    st.markdown(
        f"""
<div class="page-head">
  <div class="eyebrow">{ICONS.get(icon, '')}{eyebrow}</div>
  <h1 class="page-title">{title}</h1>
  {f'<p class="page-lede">{lede}</p>' if lede else ''}
</div>
""",
        unsafe_allow_html=True,
    )


def section(title: str, description: str = "") -> None:
    st.markdown(
        f"""
<div class="section-head">
  <div class="section-title">{title}</div>
  {f'<div class="section-desc">{description}</div>' if description else ''}
</div>
""",
        unsafe_allow_html=True,
    )


def kpi(title: str, value, icon: str = "", tone: str = "", foot: str = "",
        hint: str = "", tip: str = "") -> str:
    """Return the HTML for one KPI tile. All tiles share one fixed height."""
    icon_html = f'<span class="ag-kpi-icon">{ICONS[icon]}</span>' if icon else ""
    tip_html = _tip(tip)
    interactive = " ag-kpi--interactive" if hint else ""

    if hint:
        foot_html = (
            f'<div class="ag-kpi-foot"><span class="ag-kpi-hint">{hint} &rarr;</span></div>'
        )
    else:
        foot_html = f'<div class="ag-kpi-foot">{foot}</div>'

    return f"""
<div class="ag-card ag-kpi{interactive} {tone} ag-reveal">
  <div class="ag-kpi-top">
    <span class="ag-kpi-label">{title}</span>
    <span style="display:flex;align-items:center;gap:6px">{tip_html}{icon_html}</span>
  </div>
  <div>
    <div class="ag-kpi-value">{value}</div>
    {foot_html}
  </div>
</div>
"""


def kpi_row(items) -> None:
    """Render KPI tiles in one equal-height row."""
    cols = st.columns(len(items), gap="medium")
    for col, item in zip(cols, items):
        with col:
            st.markdown(kpi(**item), unsafe_allow_html=True)


def step_label(number: str, title: str) -> None:
    st.markdown(
        f'<div class="ag-step"><span class="ag-step-num">{number}</span>'
        f'<span class="ag-step-title">{title}</span></div>',
        unsafe_allow_html=True,
    )


def back_button(label: str = "Back to Dashboard", target: str = "Dashboard",
                key: str = "back") -> None:
    """
    Navigates by setting the shared page state, so the layout (and therefore
    the sidebar) is rendered by the same single code path on the next run.
    """
    def _go():
        st.session_state["page"] = target

    st.button(f"\u2190  {label}", key=key, on_click=_go, type="tertiary")


def legend(items) -> None:
    dots = "".join(
        f'<span class="ag-legend-item">'
        f'<span class="ag-legend-dot" style="background:{color}"></span>{label}</span>'
        for label, color in items
    )
    st.markdown(f'<div class="ag-legend">{dots}</div>', unsafe_allow_html=True)


def metric_tip(label: str, text: str) -> str:
    return f"{label} {_tip(text)}"

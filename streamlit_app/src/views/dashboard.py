"""Dashboard view."""

import plotly.graph_objects as go
import streamlit as st

from ..components import kpi_row, page_header, section
from ..data import study_time_band
from ..theme import CHART_LAYOUT, COLORS, ICONS


def _signal_row(name, sub, value, unit, risk_val, safe_val):
    return f"""
<div class="ag-row">
  <div>
    <div class="ag-row-name">{name}</div>
    <div class="ag-row-sub">{sub}</div>
  </div>
  <div>
    <div class="ag-row-val">{value}<span class="ag-row-unit">{unit}</span></div>
    <div class="ag-split">
      <span class="at-risk">At risk {risk_val}</span>
      <span class="not-at-risk">Not at risk {safe_val}</span>
    </div>
  </div>
</div>
"""


def render(ctx):
    ds, ev, insights = ctx["ds"], ctx["eval"], ctx["insights"]
    cmp_ = ds["comparison"]
    avg = ds["overall_avg"]

    page_header(
        "Academic Intelligence",
        "Academic Risk Early-Warning System",
        "Identify students who need academic support before final grades are "
        "recorded, using attendance, prior performance and study context.",
        icon="grid",
    )

    kpi_row([
        dict(title="Total Students", value=ds["total"], icon="users",
             foot="Full cohort in the dataset"),
        dict(title="At Risk", value=ds["at_risk"], icon="alert", tone="tone-risk",
             foot=f'{ds["at_risk"] / ds["total"] * 100:.1f}% of the cohort'),
        dict(title="Not At Risk", value=ds["not_at_risk"], icon="check", tone="tone-safe",
             foot=f'{ds["not_at_risk"] / ds["total"] * 100:.1f}% of the cohort'),
        dict(title="At-Risk Recall", value=f'{ev["recall"] * 100:.1f}%', icon="target",
             tone="tone-primary",
             tip="Percentage of actual at-risk students the model correctly identified "
                 "on the held-out test set.",
             foot=f'Held-out test set · {ev["test_size"]} students'),
    ])

    # ------------------------------------------------------------------
    section("Risk Overview", "Cohort split against the target definition: final grade (G3) of 11 or below is At Risk.")

    left, right = st.columns([1, 1.1], gap="medium")

    with left:
        with st.container(border=True):
            fig = go.Figure(data=[go.Pie(
                labels=["Not At Risk", "At Risk"],
                values=[ds["not_at_risk"], ds["at_risk"]],
                hole=0.66,
                sort=False,
                marker=dict(colors=[COLORS["safe"], COLORS["risk"]],
                            line=dict(color="#FFFFFF", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>Students: %{value}"
                              "<br>Share: %{percent}<extra></extra>",
            )])
            fig.update_layout(
                **CHART_LAYOUT, height=252, showlegend=False,
                annotations=[dict(
                    text=f'<b style="font-size:26px">{ds["at_risk"] / ds["total"] * 100:.0f}%</b>'
                         f'<br><span style="font-size:11px;color:#6B7280">AT RISK</span>',
                    showarrow=False, font=dict(color=COLORS["text"]),
                )],
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown(
                f'<div class="ag-legend" style="padding:0 0 4px 0">'
                f'<span class="ag-legend-item"><span class="ag-legend-dot" '
                f'style="background:{COLORS["safe"]}"></span>Not At Risk · {ds["not_at_risk"]}</span>'
                f'<span class="ag-legend-item"><span class="ag-legend-dot" '
                f'style="background:{COLORS["risk"]}"></span>At Risk · {ds["at_risk"]}</span></div>',
                unsafe_allow_html=True,
            )

    with right:
        with st.container(border=True):
            st.markdown(
                '<div style="padding:4px 4px 0 4px"><div class="ag-kpi-label">Academic Signals</div>'
                '<div class="ag-row-sub" style="margin-bottom:6px">Cohort averages, split by risk group</div>',
                unsafe_allow_html=True,
            )
            rows = [
                ("Absences", "Classes missed", f'{avg["absences"]:.1f}', "days",
                 f'{cmp_.loc["absences", "At Risk"]:.1f}', f'{cmp_.loc["absences", "Not At Risk"]:.1f}'),
                ("Study Time", study_time_band(avg["studytime"]), f'{avg["studytime"]:.2f}', "/ 4",
                 f'{cmp_.loc["studytime", "At Risk"]:.2f}', f'{cmp_.loc["studytime", "Not At Risk"]:.2f}'),
                ("Failures", "Previously failed classes", f'{avg["failures"]:.2f}', "",
                 f'{cmp_.loc["failures", "At Risk"]:.2f}', f'{cmp_.loc["failures", "Not At Risk"]:.2f}'),
                ("G1", "First period grade", f'{avg["G1"]:.1f}', "/ 20",
                 f'{cmp_.loc["G1", "At Risk"]:.1f}', f'{cmp_.loc["G1", "Not At Risk"]:.1f}'),
                ("G2", "Second period grade", f'{avg["G2"]:.1f}', "/ 20",
                 f'{cmp_.loc["G2", "At Risk"]:.1f}', f'{cmp_.loc["G2", "Not At Risk"]:.1f}'),
            ]
            st.markdown(
                '<div class="ag-rows">' + "".join(_signal_row(*r) for r in rows) + "</div></div>",
                unsafe_allow_html=True,
            )

    # ------------------------------------------------------------------
    section("Key Insights", "Derived directly from the loaded dataset.")
    body = "".join(
        f'<div class="ag-insight"><span class="ag-insight-mark">{i + 1:02d}</span>'
        f'<div><div class="ag-insight-label">{item["label"]}</div>'
        f'<div class="ag-insight-text">{item["text"]}</div></div></div>'
        for i, item in enumerate(insights)
    )
    with st.container(border=True):
        st.markdown(f'<div style="padding:4px">{body}</div>', unsafe_allow_html=True)

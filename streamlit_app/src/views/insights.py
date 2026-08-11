"""Dataset Insights view."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ..components import back_button, kpi_row, page_header, section
from ..theme import CHART_LAYOUT, COLORS, style_axes
from ..config import RISK_THRESHOLD_G3


def render(ctx):
    ds = ctx["ds"]

    back_button(key="back_insights")
    page_header(
        "Data Exploration",
        "Dataset Insights",
        "Structure and distribution of the student cohort used to train and "
        "evaluate the model.",
        icon="database",
    )

    kpi_row([
        dict(title="Students", value=ds["total"], icon="users", foot="Records in the dataset"),
        dict(title="Features", value=ds["n_columns"], icon="database",
             foot=f'{ds["n_features_used"]} used by the model'),
        dict(title="At-Risk Students", value=ds["at_risk"], icon="alert", tone="tone-risk",
             foot=f'{ds["at_risk"] / ds["total"] * 100:.1f}% of the cohort'),
        dict(title="Not At-Risk Students", value=ds["not_at_risk"], icon="check",
             tone="tone-safe", foot=f'{ds["not_at_risk"] / ds["total"] * 100:.1f}% of the cohort'),
    ])

    section(
        "Final Grade Distribution",
        f"Students scoring G3 ≤ {RISK_THRESHOLD_G3} are labelled At Risk.",
    )
    gc = ds["grade_counts"]
    with st.container(border=True):
        fig = go.Figure(data=[go.Bar(
            x=gc["Grade"], y=gc["Count"],
            marker_color=[COLORS["risk"] if s == "At Risk" else COLORS["safe"] for s in gc["Status"]],
            customdata=gc[["Percent", "Status"]],
            hovertemplate="<b>Grade: %{x}</b><br>Students: %{y}"
                          "<br>Percentage: %{customdata[0]:.1f}%"
                          "<br>Class: %{customdata[1]}<extra></extra>",
        )])
        fig.update_layout(**CHART_LAYOUT, height=340, bargap=0.25)
        style_axes(fig, y_title="Students", x_title="Final grade (G3)")
        fig.update_xaxes(tickmode="linear", tick0=0, dtick=1)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f'<div class="ag-legend" style="padding:0 0 6px 4px">'
            f'<span class="ag-legend-item"><span class="ag-legend-dot" '
            f'style="background:{COLORS["risk"]}"></span>At Risk (G3 ≤ {RISK_THRESHOLD_G3})</span>'
            f'<span class="ag-legend-item"><span class="ag-legend-dot" '
            f'style="background:{COLORS["safe"]}"></span>Not At Risk (G3 ≥ {RISK_THRESHOLD_G3 + 1})</span></div>',
            unsafe_allow_html=True,
        )

    section("Academic Indicators", "Average feature values for each risk group.")
    tab_chart, tab_table = st.tabs(["Chart", "Table"])
    with tab_chart:
        fig_i = px.bar(
            ds["avg_melt"], x="variable", y="value", color="Risk Status", barmode="group",
            color_discrete_map={"Not At Risk": COLORS["safe"], "At Risk": COLORS["risk"]},
        )
        fig_i.update_traces(
            hovertemplate="<b>%{x}</b><br>Average: %{y:.2f}<extra></extra>")
        fig_i.update_layout(
            **CHART_LAYOUT, height=340,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        title="", font=dict(color=COLORS["sub"])),
        )
        style_axes(fig_i, y_title="Average value")
        st.plotly_chart(fig_i, use_container_width=True, config={"displayModeBar": False})
    with tab_table:
        st.dataframe(ds["comparison"].style.format("{:.2f}"), use_container_width=True)

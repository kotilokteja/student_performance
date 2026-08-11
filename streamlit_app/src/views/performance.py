"""Model Performance view."""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ..components import back_button, kpi_row, page_header, section
from ..data import get_deployed_model_name, get_model_comparison
from ..theme import CHART_LAYOUT, COLORS, style_axes

TIPS = {
    "Accuracy": "Percentage of predictions that were correct on the test set.",
    "Precision": "Of all students predicted At Risk, the percentage that truly are At Risk.",
    "Recall": "Percentage of actual at-risk students correctly identified.",
    "F1 Score": "Harmonic mean of precision and recall.",
}

CELL_MEANING = [
    ["True Negative — correctly cleared", "False Positive — flagged but not at risk"],
    ["False Negative — missed at-risk student", "True Positive — correctly flagged at risk"],
]


def render(ctx):
    ev, df = ctx["eval"], ctx["df"]

    back_button(key="back_performance")
    page_header(
        "Model Evaluation",
        "Model Performance",
        f'Evaluated on a held-out test set of {ev["test_size"]} students '
        "(20% stratified split, random state 42).",
        icon="chart",
    )

    kpi_row([
        dict(title="Accuracy", value=f'{ev["accuracy"] * 100:.1f}%', tip=TIPS["Accuracy"]),
        dict(title="Precision", value=f'{ev["precision"] * 100:.1f}%', tip=TIPS["Precision"]),
        dict(title="Recall", value=f'{ev["recall"] * 100:.1f}%', tip=TIPS["Recall"],
             tone="tone-primary"),
        dict(title="F1 Score", value=f'{ev["f1"] * 100:.1f}%', tip=TIPS["F1 Score"]),
    ])

    section("Confusion Matrix", "Predictions on the held-out test set. Hover a cell for its meaning.")
    cm = ev["cm"]
    with st.container(border=True):
        fig = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale=[[0, "#EFF6FF"], [1, "#2563EB"]],
            x=["Not At Risk", "At Risk"],
            y=["Not At Risk", "At Risk"],
        )
        fig.update_traces(
            customdata=CELL_MEANING,
            hovertemplate="<b>%{customdata}</b><br>Actual: %{y}<br>"
                          "Predicted: %{x}<br>Students: %{z}<extra></extra>",
            textfont=dict(size=18),
        )
        fig.update_layout(**CHART_LAYOUT, height=360, coloraxis_showscale=False)
        style_axes(fig, y_title="Actual class", x_title="Predicted class")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    deployed = get_deployed_model_name()
    section(
        "Algorithm Comparison",
        f"All three candidate algorithms trained on the same split. "
        f"{deployed} is the deployed model.",
    )
    comparison = get_model_comparison(df)
    with st.container(border=True):
        palette = {"Accuracy": COLORS["primary"], "Precision": "#93C5FD",
                   "Recall": COLORS["safe"], "F1 Score": "#9CA3AF"}
        fig_c = go.Figure()
        for metric, color in palette.items():
            fig_c.add_trace(go.Bar(
                x=comparison["Model"], y=comparison[metric], name=metric,
                marker_color=color,
                hovertemplate="<b>%{x}</b><br>" + metric + ": %{y:.3f}<extra></extra>",
            ))
        fig_c.update_layout(
            **CHART_LAYOUT, barmode="group", height=360,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        title="", font=dict(color=COLORS["sub"])),
        )
        fig_c.update_yaxes(range=[0, 1.05])
        style_axes(fig_c, y_title="Score")
        st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})
        st.dataframe(
            comparison.set_index("Model").style.format("{:.3f}"),
            use_container_width=True,
        )

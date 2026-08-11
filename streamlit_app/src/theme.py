"""
Frontend asset loading (CSS/JS) and the shared icon set.

Assets are read from ./frontend and cached, so no repeated disk IO happens
across reruns. CSS is injected exactly once per script run.
"""

import streamlit as st
import streamlit.components.v1 as components

from .config import FRONTEND_DIR


@st.cache_data(show_spinner=False)
def _read(name: str) -> str:
    path = FRONTEND_DIR / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def inject_frontend(enable_js: bool = True) -> None:
    """Inject the stylesheet (and optional progressive-enhancement script)."""
    raw = _read("styles.css") + "\n" + _read("components.css")
    # Streamlit ends a raw-HTML block at the first blank line, which would
    # dump the rest of the stylesheet onto the page as text. Strip blanks.
    css = "\n".join(line for line in raw.splitlines() if line.strip())
    st.markdown(
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" '
        'href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">'
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
    if enable_js:
        js = _read("interactions.js")
        if js:
            components.html(f"<script>{js}</script>", height=0, width=0)


# ---------------------------------------------------------------------------
# Icons — one consistent 1.5px stroke set (Feather-style), no emoji anywhere.
# ---------------------------------------------------------------------------
def _svg(body: str, size: int = 18) -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


ICONS = {
    "users": _svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
                  '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    "alert": _svg('<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
                  '<line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'),
    "check": _svg('<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'),
    "target": _svg('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>'),
    "grid": _svg('<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/>'
                 '<rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>'),
    "clipboard": _svg('<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
                      '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="m9 14 2 2 4-4"/>'),
    "database": _svg('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>'
                     '<path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'),
    "chart": _svg('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>'
                  '<line x1="6" y1="20" x2="6" y2="14"/>'),
    "info": _svg('<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/>'
                 '<line x1="12" y1="8" x2="12.01" y2="8"/>'),
    "arrow_left": _svg('<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>', 16),
    "clock": _svg('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
    "file": _svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
                 '<polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/>'
                 '<line x1="16" y1="17" x2="8" y2="17"/>', 48),
    "book": _svg('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
                 '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'),
    "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
}

NAV_ICONS = {
    "Dashboard": "grid",
    "Risk Assessment": "clipboard",
    "Model Performance": "chart",
    "Dataset Insights": "database",
    "About": "book",
}

# Shared Plotly styling so every chart matches the design system.
CHART_FONT = dict(family="Inter, system-ui, sans-serif", color="#111827", size=12)
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=CHART_FONT,
    margin=dict(t=16, b=16, l=16, r=16),
    hoverlabel=dict(
        bgcolor="#111827",
        font=dict(color="#FFFFFF", family="Inter, system-ui, sans-serif", size=12),
        bordercolor="#111827",
    ),
)

COLORS = {
    "primary": "#2563EB",
    "risk": "#DC2626",
    "safe": "#15803D",
    "muted": "#9CA3AF",
    "grid": "#E5E7EB",
    "text": "#111827",
    "sub": "#4B5563",
}


def style_axes(fig, y_title: str = "", x_title: str = ""):
    fig.update_xaxes(
        title_text=x_title, showgrid=False, linecolor=COLORS["grid"],
        tickfont=dict(color=COLORS["sub"]), title_font=dict(color=COLORS["sub"], size=12),
    )
    fig.update_yaxes(
        title_text=y_title, gridcolor=COLORS["grid"], zeroline=False, linecolor="rgba(0,0,0,0)",
        tickfont=dict(color=COLORS["sub"]), title_font=dict(color=COLORS["sub"], size=12),
    )
    return fig

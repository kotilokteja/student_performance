"""
Aegis — Academic Risk Early-Warning System
==========================================
Single application shell. The sidebar and the page body are rendered by this
one code path on every run, so navigation (including Back buttons) can never
hide or duplicate the sidebar.

All ML behaviour lives in src/data.py and is unchanged from the original
project: same dataset, same target (G3 <= 11), same features, same saved
pipeline, same probability, same evaluation.
"""

import streamlit as st

from src.config import APP_NAME, APP_TAGLINE, APP_VERSION, NAV_GROUPS, DEFAULT_PAGE
from src.state import init_session_state, goto
from src.theme import inject_frontend, ICONS, NAV_ICONS
from src.data import bootstrap
from src.views import REGISTRY

st.set_page_config(
    page_title="Aegis | Academic Risk Early-Warning System",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_frontend()


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            f"""
<div class="brand">
  <div class="brand-mark">{APP_NAME[0]}</div>
  <div>
    <div class="brand-name">{APP_NAME}</div>
    <div class="brand-sub">{APP_TAGLINE}</div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        current = st.session_state.get("page", DEFAULT_PAGE)
        for group, pages in NAV_GROUPS:
            st.markdown(f'<div class="nav-group-label">{group}</div>', unsafe_allow_html=True)
            for page in pages:
                st.button(
                    page,
                    key=f"nav_{page}",
                    on_click=goto,
                    args=(page,),
                    use_container_width=True,
                    type="primary" if page == current else "tertiary",
                )

        st.markdown(
            f'<div class="sidebar-foot">Version {APP_VERSION}<br>'
            f'Screening signal for human review.</div>',
            unsafe_allow_html=True,
        )


render_sidebar()

ctx = bootstrap()
page = st.session_state.get("page", DEFAULT_PAGE)
REGISTRY.get(page, REGISTRY[DEFAULT_PAGE])(ctx)

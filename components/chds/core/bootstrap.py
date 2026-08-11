import streamlit as st
from components.chds.shell.sidebar import render_sidebar
from components.chds.theme import inject_theme


def bootstrap(
    title="CardHawkOS™",
    icon="🦅",
    layout="wide",
):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded",
    )

    inject_theme()
    render_sidebar()

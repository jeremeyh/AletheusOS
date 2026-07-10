import streamlit as st

from cardhawk_platform.startup import bootstrap_cardhawk
from cardhawk_platform.navigation import render_sidebar_navigation
from cardhawk_platform.router import render_route
from themes.cardhawk_theme import apply_cardhawk_theme

st.set_page_config(
    page_title="CardHawk OS™",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_cardhawk_theme()

state = bootstrap_cardhawk()
route = render_sidebar_navigation(state)
render_route(route, state)

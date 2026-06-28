import streamlit as st

from kernel.runtime import kernel
from themes.cardhawk_theme import apply_cardhawk_theme

st.set_page_config(
    page_title="CardHawk OS™",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_cardhawk_theme()

kernel.boot()

st.title("🦅 CardHawk OS™")
st.caption("Intelligence Fabric™ Runtime")

status = kernel.status()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Engines", status["engines"])
c2.metric("Services", status["services"])
c3.metric("Projections", status["projections"])
c4.metric("Listeners", sum(status["listeners"].values()))

st.divider()

st.success("CardHawk OS™ Kernel is running.")

st.subheader("Runtime Status")

st.json(status)

st.info(
    "The legacy navigation system has been temporarily bypassed while "
    "the application is migrated to the new Kernel architecture."
)

import streamlit as st
from components.live_platform_ui import hero
from services.live_platform_service import LivePlatformService


def render(state):
    assets = LivePlatformService.assets(state)
    hero()
    st.title("🧬 Portfolio Digital Twin™")

    ask = st.number_input("Candidate Purchase Price", 0.0, value=250.0)
    est = st.number_input("Estimated Current Value", 0.0, value=400.0)

    try:
        from portfolio_digital_twin.digital_twin_service import PortfolioDigitalTwin
        if st.button("Simulate Portfolio Impact"):
            st.json(PortfolioDigitalTwin.simulate_add(assets, ask, est))
    except Exception:
        st.info("Digital Twin service staged.")

import streamlit as st

from portfolio.digital_twin.engine import PortfolioDigitalTwin

st.set_page_config(
    page_title="CardHawk OS™",
    page_icon="🦅",
    layout="wide",
)

snapshot = PortfolioDigitalTwin.snapshot()

st.title("🦅 CardHawk OS™")
st.caption("Collectible Intelligence Platform")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Portfolio",
    f"${snapshot['total_value']:,.2f}"
)

c2.metric(
    "Gain/Loss",
    f"${snapshot['gain_loss']:,.2f}"
)

c3.metric(
    "Assets",
    snapshot["asset_count"]
)

c4.metric(
    "Avg THORᵡ",
    snapshot["average_thorx"]
)

st.divider()

left, right = st.columns([2, 1])

with left:

    st.subheader("Mission Status")

    st.success("CardHawk OS™ operational")

    st.write("Registered Engines")

    st.code(
        """
✓ Hawk A•Eye™
✓ THORᵡ
✓ Marketplace Intelligence™
✓ Negotiation AI™
✓ Founder AI™
✓ Portfolio Digital Twin™
✓ Founder Copilot™
"""
    )

with right:

    st.subheader("Quick Actions")

    st.page_link(
        "pages/01_Asset_Intake.py",
        label="Asset Intake™"
    )

    st.page_link(
        "pages/03_Asset_Explorer.py",
        label="Asset Explorer™"
    )

    st.page_link(
        "pages/04_Asset_Intelligence.py",
        label="Asset Intelligence™"
    )

    st.page_link(
        "pages/98_Command_Center.py",
        label="Mission Control™"
    )

"""
Card Hawk Web Application

Version 5.0.0
"""

import streamlit as st
from cardhawk.dashboard import DashboardService
from cardhawk.services import AssetService

st.set_page_config(
    page_title="Card Hawk",
    page_icon="🦅",
    layout="wide",
)

dashboard = DashboardService()
service = AssetService()

snapshot = dashboard.snapshot()
assets = service.list_assets()

st.title("🦅 Card Hawk")

left, right = st.columns(2)

with left:
    st.metric(
        "Assets",
        snapshot["portfolio"]["asset_count"],
    )

    st.metric(
        "Purchase Total",
        f"${snapshot['portfolio']['purchase_total']:,.2f}",
    )

with right:
    st.metric(
        "Market Value",
        f"${snapshot['portfolio']['market_total']:,.2f}",
    )

    st.metric(
        "Gain / Loss",
        f"${snapshot['portfolio']['unrealized_gain']:,.2f}",
    )

st.divider()

st.subheader("Asset Vault")

if assets:
    rows = []

    for asset in assets:
        rows.append(
            {
                "Player": asset.player,
                "Team": asset.team,
                "Category": asset.category,
                "Purchase": asset.purchase_price,
                "Value": asset.estimated_value,
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No assets have been added yet.")

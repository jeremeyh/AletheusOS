import streamlit as st
from components.chds.asset_card import render_asset_card


def render_engine_status():
    st.success("CardHawk OS™ Operational")

    engines = [
        "Hawk A•Eye™",
        "THORᵡ™",
        "Marketplace Intelligence™",
        "Negotiation AI™",
        "Founder AI™",
        "Portfolio Digital Twin™",
        "Founder Copilot™",
        "Event Bus™",
        "Timeline™",
    ]

    for engine in engines:
        c1, c2 = st.columns([4, 1])

        with c1:
            st.write(engine)

        with c2:
            st.success("●")


def render_top_assets(snapshot, limit=6):
    assets = snapshot.get("top_assets", [])[:limit]

    if not assets:
        st.info("No assets found.")
        return

    for asset in assets:
        render_asset_card(asset)


def render_allocation(snapshot):
    allocation = snapshot.get("allocation_by_player", {})
    total = float(snapshot.get("total_value") or 1)

    if not allocation:
        st.info("No allocation data.")
        return

    for player, value in allocation.items():
        pct = float(value or 0) / total

        st.write(f"**{player}** — ${float(value):,.2f}")
        st.progress(max(0.0, min(pct, 1.0)))

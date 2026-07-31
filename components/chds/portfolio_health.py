import streamlit as st


def render_portfolio_health(snapshot):
    """
    CardHawkOS Portfolio Health™
    """

    assets = snapshot.get("assets", [])

    if not assets:
        st.info("No portfolio health data available.")
        return

    total_assets = len(assets)

    high_thorx = [
        asset for asset in assets if float(asset.get("thorx_score") or 0) >= 80
    ]

    undervalued = [
        asset
        for asset in assets
        if float(asset.get("current_value") or 0)
        > float(asset.get("purchase_price") or 0)
        and float(asset.get("purchase_price") or 0) > 0
    ]

    graded = [asset for asset in assets if asset.get("grade")]

    high_thorx_pct = 0
    undervalued_pct = 0
    graded_pct = 0

    if total_assets:
        high_thorx_pct = len(high_thorx) / total_assets * 100
        undervalued_pct = len(undervalued) / total_assets * 100
        graded_pct = len(graded) / total_assets * 100

    st.subheader("🧬 Portfolio Health™")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "High THORᵡ Assets",
            f"{high_thorx_pct:.0f}%",
        )

    with c2:
        st.metric(
            "Positive ROI Assets",
            f"{undervalued_pct:.0f}%",
        )

    with c3:
        st.metric(
            "Graded Assets",
            f"{graded_pct:.0f}%",
        )

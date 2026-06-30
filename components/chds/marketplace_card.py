import streamlit as st


def render_marketplace_card(snapshot):
    """
    CardHawkOS Marketplace Intelligence Card™
    """

    market = snapshot.get("market", snapshot)

    st.subheader("💰 Marketplace Intelligence™")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Current Value",
            f"${float(market.get('current_value') or 0):,.2f}",
        )

    with c2:
        st.metric(
            "Average Sale",
            f"${float(market.get('average_sale') or 0):,.2f}",
        )

    with c3:
        st.metric(
            "High Sale",
            f"${float(market.get('highest_sale') or 0):,.2f}",
        )

    with c4:
        st.metric(
            "Low Sale",
            f"${float(market.get('lowest_sale') or 0):,.2f}",
        )

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "Comps",
            market.get("comp_count", 0),
        )

    with c6:
        st.metric(
            "Confidence",
            f"{market.get('confidence', 0)}%",
        )

    with c7:
        st.metric(
            "Velocity",
            market.get("market_velocity", "Unknown"),
        )

    comps = market.get("comps", [])

    if comps:
        with st.expander("View Comparable Sales"):
            st.dataframe(
                comps,
                width="stretch",
                hide_index=True,
            )

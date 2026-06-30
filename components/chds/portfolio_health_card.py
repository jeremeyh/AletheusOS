import streamlit as st


def render_portfolio_health_card(snapshot):
    """
    CardHawkOS Portfolio Health Card™
    """

    st.subheader("🧬 Portfolio Health™")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "Assets",
            snapshot.get("asset_count", 0),
        )

    with c2:
        st.metric(
            "Portfolio",
            f"${float(snapshot.get('value') or 0):,.2f}",
        )

    with c3:
        st.metric(
            "Gain / Loss",
            f"${float(snapshot.get('gain') or 0):,.2f}",
        )

    with c4:
        st.metric(
            "ROI",
            f"{float(snapshot.get('roi') or 0):.2f}%",
        )

    with c5:
        st.metric(
            "Avg THORᵡ",
            f"{float(snapshot.get('avg_thorx') or 0):.2f}",
        )


# Backwards compatibility
render_portfolio_health = render_portfolio_health_card

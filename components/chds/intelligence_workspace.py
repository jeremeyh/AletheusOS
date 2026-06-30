import streamlit as st


def render_intelligence_workspace(result):
    """
    CardHawkOS Intelligence Workspace™

    Unified analyst view for a single asset.
    """

    st.subheader("🧠 Intelligence Workspace™")

    card = result.get("hawk", {}).get("card", {})
    market = result.get("market", {})
    negotiation = result.get("negotiation", {})
    founder = result.get("founder", {})
    thorx = result.get("thorx", 0)

    left, right = st.columns([1, 1])

    with left:

        st.markdown("### Asset")

        st.write(f"**Player:** {card.get('player','Unknown')}")
        st.write(f"**Brand:** {card.get('brand','')}")
        st.write(f"**Set:** {card.get('set','')}")
        st.write(f"**Parallel:** {card.get('parallel','')}")
        st.write(f"**Grade:** {card.get('grade','Raw')}")

        st.metric(
            "THORᵡ",
            f"{thorx:.1f}",
        )

    with right:

        st.markdown("### Market")

        st.metric(
            "Market Value",
            f"${market.get('current_value',0):,.2f}",
        )

        st.metric(
            "Confidence",
            f"{market.get('confidence',0)}%",
        )

        st.metric(
            "Maximum Offer",
            f"${negotiation.get('maximum_offer',0):,.2f}",
        )

        st.metric(
            "ROI",
            f"{negotiation.get('expected_roi',0):.2f}%",
        )

    st.divider()

    st.markdown("### Founder AI™")

    st.info(
        founder.get(
            "summary",
            "No Founder AI summary available.",
        )
    )

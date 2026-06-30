import streamlit as st


def render_market_widget():

    st.subheader("💰 Marketplace")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Average",
            "$124.50",
        )

        st.metric(
            "Floor",
            "$121",
        )

    with c2:
        st.metric(
            "Ceiling",
            "$129",
        )

        st.metric(
            "Confidence",
            "80%",
        )

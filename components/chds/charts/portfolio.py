import streamlit as st
import pandas as pd


def render_portfolio_chart(snapshot):
    """
    Portfolio Overview Chart
    """

    allocation = snapshot.get("allocation_by_player", {})

    if not allocation:
        st.info("No portfolio data available.")
        return

    data = pd.DataFrame(
        {
            "Player": list(allocation.keys()),
            "Value": list(allocation.values()),
        }
    )

    st.subheader("📈 Portfolio Allocation")

    st.bar_chart(
        data.set_index("Player"),
        height=350,
        width="stretch",
    )

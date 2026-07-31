import streamlit as st

from analytics.analytics_service import PortfolioAnalyticsService


def render(state):
    st.title("📊 Portfolio Analytics™")
    svc = state["container"].service("assets")
    assets = svc.get_all() if svc else []

    tabs = st.tabs(
        [
            "Allocation",
            "Concentration",
            "Risk",
            "Capital Efficiency",
            "Scenario Comparison",
        ]
    )

    with tabs[0]:
        field = st.selectbox(
            "Allocation Field", ["sport", "team", "brand", "category", "player"]
        )
        data = PortfolioAnalyticsService.allocation(assets, field)
        st.bar_chart(data)
        st.json(data)

    with tabs[1]:
        field = st.selectbox(
            "Concentration Field", ["player", "team", "brand", "sport"], key="conc"
        )
        st.json(PortfolioAnalyticsService.distribution(assets, field))

    with tabs[2]:
        st.json(PortfolioAnalyticsService.risk_distribution(assets))

    with tabs[3]:
        st.dataframe(
            PortfolioAnalyticsService.capital_efficiency(assets),
            use_container_width=True,
        )

    with tabs[4]:
        st.info("Scenario comparison connects to Digital Twin 2.0™.")

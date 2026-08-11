import streamlit as st
from components.live_platform_ui import (
    action_rows,
    asset_rows,
    founder_brief,
    hero,
    kpis,
    marketplace_rows,
    panel,
)
from services.live_platform_service import LivePlatformService


def render(state):
    data = LivePlatformService.dashboard(state)
    hero()
    kpis(data["summary"])

    st.divider()

    left, right = st.columns([1.2, 1])
    with left:
        founder_brief(data["brief"])
    with right:
        panel("Daily Actions™", action_rows(data["actions"]))

    st.divider()

    chart_col, market_col = st.columns([1.2, 1])
    with chart_col:
        st.markdown(
            '<div class="ch-panel"><div class="ch-panel-title">Portfolio Performance™</div>',
            unsafe_allow_html=True,
        )
        value = data["summary"]["portfolio_value"]
        if value > 0:
            st.line_chart(
                [value * x for x in [0.82, 0.86, 0.91, 0.89, 0.95, 1.0]], height=260
            )
        else:
            st.markdown(
                '<span class="ch-muted">Add assets to activate live chart.</span>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    with market_col:
        panel("Marketplace Intelligence™", marketplace_rows(data["marketplace"]))

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        panel("THORᵡ Leaders™", asset_rows(data["ranked"], "thorx"))
    with c2:
        panel("Top Movers™", asset_rows(data["movers"], "roi"))

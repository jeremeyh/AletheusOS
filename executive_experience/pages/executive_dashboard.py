import streamlit as st
from components.executive_ui import (
    activity_rows,
    asset_rows,
    founder_brief_card,
    hero,
    marketplace_rows,
    metric_cards,
    panel,
    task_rows,
)
from services.executive_experience_service import ExecutiveExperienceService


def render(state):
    data = ExecutiveExperienceService.build_dashboard(state)

    hero()
    metric_cards(data["summary"])

    st.divider()

    left, right = st.columns([1.2, 1])
    with left:
        founder_brief_card(data["brief"])
    with right:
        panel("Daily Operating Queue™", task_rows(data["tasks"]))

    st.divider()

    chart_col, allocation_col = st.columns([1.2, 1])
    with chart_col:
        st.markdown(
            '<div class="ch-panel"><div class="ch-panel-title">Portfolio Performance™</div>',
            unsafe_allow_html=True,
        )
        value = data["summary"]["portfolio_value"]
        if value > 0:
            st.line_chart(
                [value * x for x in [0.80, 0.84, 0.88, 0.92, 0.90, 0.96, 1.0]],
                height=260,
            )
        else:
            st.markdown(
                '<span class="ch-muted">Add assets to activate live performance chart.</span>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    with allocation_col:
        panel("Live Intelligence Layer™", activity_rows(data["activity"]))

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        panel("THORᵡ Leaders™", asset_rows(data["ranked"], "thorx"))
    with c2:
        panel("Top Movers™", asset_rows(data["movers"], "roi"))

    st.divider()

    panel("Marketplace Opportunity Board™", marketplace_rows(data["marketplace"]))

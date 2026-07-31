import streamlit as st

from founder_studio.studio_service import FounderStudioService


def render(state):
    st.title("🦅 Founder Intelligence Studio™")
    FounderStudioService.seed_defaults()

    item_type = st.selectbox(
        "Studio Section",
        [
            "Investment Thesis",
            "Watchlist",
            "Capital Plan",
            "Decision Journal",
            "Monthly Review",
            "Quarterly Review",
            "Opportunity Backlog",
            "Conviction Ranking",
            "Goal Tracking",
        ],
    )

    with st.expander("Create Studio Item", expanded=False):
        title = st.text_input("Title")
        body = st.text_area("Body")
        if st.button("Save Studio Item"):
            FounderStudioService.create(item_type, title, body)
            st.success("Saved.")

    st.divider()
    for item in FounderStudioService.all(item_type):
        with st.container(border=True):
            st.write(f"**{item.title}**")
            st.caption(f"{item.item_type} • {item.status} • {item.created_at}")
            st.write(item.body)

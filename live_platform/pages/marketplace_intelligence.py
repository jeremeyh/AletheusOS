import streamlit as st
from components.live_platform_ui import hero
from services.live_platform_service import LivePlatformService


def render(state):
    data = LivePlatformService.dashboard(state)
    hero()
    st.title("🌐 Marketplace Intelligence™")

    q = st.text_input("Search normalized marketplace feed", "")
    min_score = st.slider("Minimum Opportunity Score", 0.0, 10.0, 0.0)

    items = data["marketplace"]
    for item in items:
        if q and q.lower() not in item["title"].lower():
            continue
        if item["score"] < min_score:
            continue
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{item['title']}**")
            c1.caption(item["source"])
            c2.metric("Opportunity", item["score"])
            c3.write(item["recommendation"])

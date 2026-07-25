import streamlit as st
from components.executive_ui import hero
from services.executive_experience_service import ExecutiveExperienceService


def render(state):
    data = ExecutiveExperienceService.build_dashboard(state)
    hero()
    st.title("🌐 Marketplace Opportunity Board™")

    q = st.text_input("Search opportunities")
    min_score = st.slider("Minimum Opportunity Score", 0.0, 10.0, 0.0)

    for item in data["marketplace"]:
        if q and q.lower() not in item["title"].lower():
            continue
        if item["opportunity_score"] < min_score:
            continue
        with st.container(border=True):
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            c1.markdown(f"### {item['title']}")
            c1.caption(item["source"])
            c2.metric("Opp Score", item["opportunity_score"])
            c3.metric("THORᵡ", item["thorx"])
            c4.write(item["recommendation"])

import streamlit as st
from timeline.timeline_service import IntelligenceTimelineService

def render(state):
    st.title("🧬 Intelligence Timeline™")
    subject = st.text_input("Asset ID / Subject", "CardHawk OS™")

    c1, c2 = st.columns(2)
    with c1:
        event_type = st.selectbox("Event Type", ["Acquisition", "Value Change", "THORᵡ Revision", "Hawk A•Eye Scan", "Note", "Marketplace Observation", "Offer", "Sale", "Thesis Revision", "Exit Recommendation"])
    with c2:
        title = st.text_input("Title", "Timeline event")

    detail = st.text_area("Detail")
    if st.button("Record Timeline Event"):
        IntelligenceTimelineService.record(subject, event_type, title, detail)
        st.success("Event recorded.")

    st.divider()
    for e in reversed(IntelligenceTimelineService.for_subject(subject)):
        with st.container(border=True):
            st.write(f"**{e.event_type}: {e.title}**")
            st.caption(e.created_at)
            st.write(e.detail)

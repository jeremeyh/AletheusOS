import streamlit as st
from operations_live.operations_service import LiveOperationsService


def render(state):
    st.title("🛰️ Live Operations Center™")
    data = LiveOperationsService.snapshot(state)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Database", data["database_health"])
    c2.metric("Pipeline", data["pipeline_execution"])
    c3.metric("Latency", f"{data['intelligence_latency_ms']} ms")
    c4.metric("Errors", len(data["errors"]))

    st.divider()
    st.subheader("Provider Health")
    st.json(data["provider_health"])
    st.subheader("Services")
    st.json(data["services"])
    st.subheader("Queue Status")
    st.json(data["queue_status"])
    if data["errors"]:
        st.subheader("Startup Errors")
        st.json(data["errors"])

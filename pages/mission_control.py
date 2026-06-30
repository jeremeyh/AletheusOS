import pandas as pd
import streamlit as st

from services.runtime_v3 import runtime_v3

st.set_page_config(page_title="Mission Control | CardHawkOS", page_icon="🛰️", layout="wide")

st.title("🛰️ Mission Control")
st.caption("Live command, telemetry, event sourcing, and plugin status for CardHawkOS Runtime v3")

health = runtime_v3.command_bus.dispatch("runtime.health").results.get("health", {})
registry = runtime_v3.command_bus.dispatch("runtime.registry").results.get("registry", {})
metrics = runtime_v3.command_bus.dispatch("runtime.metrics").results.get("metrics", [])
events = runtime_v3.command_bus.dispatch("runtime.events", {"limit": 50}).results.get("events", [])

left, right = st.columns([1, 2])

with left:
    st.subheader("System")
    st.json(health)
    if st.button("Snapshot Runtime"):
        st.json(runtime_v3.command_bus.dispatch("runtime.snapshot").results)

with right:
    st.subheader("Plugin Fleet")
    st.dataframe(pd.DataFrame(registry.get("plugins", [])), use_container_width=True)

st.divider()

st.subheader("Recent Events")
st.dataframe(pd.DataFrame(events), use_container_width=True)

st.subheader("Recent Metrics")
st.dataframe(pd.DataFrame(metrics), use_container_width=True)

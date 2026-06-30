import pandas as pd
import streamlit as st

from services.runtime_v3 import runtime_v3

st.set_page_config(page_title="Founder Console | CardHawkOS", page_icon="🦅", layout="wide")

st.title("🦅 Founder Console")
st.caption("CardHawkOS Runtime v3 — Founder command center")

health_context = runtime_v3.command_bus.dispatch("runtime.health")
health = health_context.results.get("health", {})

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Runtime", health.get("status", "unknown"))
c2.metric("Plugins", health.get("plugins", 0))
c3.metric("Enabled", health.get("enabled_plugins", 0))
c4.metric("Jobs", health.get("jobs", 0))
c5.metric("Cache Keys", health.get("cache_keys", 0))

st.divider()

tabs = st.tabs(["Health", "Registry", "Pipeline", "Scheduler", "Events", "Metrics", "Founder Memory"])

with tabs[0]:
    st.subheader("Runtime Health")
    st.json(health)

with tabs[1]:
    st.subheader("Runtime Registry")
    registry_context = runtime_v3.command_bus.dispatch("runtime.registry")
    registry = registry_context.results.get("registry", {})
    st.markdown("### Plugins")
    st.dataframe(pd.DataFrame(registry.get("plugins", [])), use_container_width=True)
    st.markdown("### Commands")
    st.dataframe(pd.DataFrame({"Command": registry.get("commands", [])}), use_container_width=True)
    st.markdown("### Jobs")
    jobs = registry.get("jobs", {})
    st.dataframe(pd.DataFrame([{"Job": k, **v} for k, v in jobs.items()]), use_container_width=True)

with tabs[2]:
    st.subheader("Runtime Intelligence Pipeline")
    asset_name = st.text_input("Asset / Opportunity", "Sample Caleb Williams Opportunity")
    player = st.text_input("Player", "Caleb Williams")
    price = st.number_input("Price", min_value=0.0, value=150.0, step=5.0)
    serial = st.text_input("Serial", "/25")
    rookie = st.checkbox("Rookie", value=True)
    auto = st.checkbox("Autograph", value=True)
    patch = st.checkbox("Patch", value=False)

    if st.button("Run Runtime v3 Pipeline", type="primary"):
        context = runtime_v3.command_bus.dispatch("runtime.pipeline", {
            "asset_name": asset_name,
            "player": player,
            "price": price,
            "serial": serial,
            "rookie": rookie,
            "auto": auto,
            "patch": patch,
        })
        if context.errors:
            st.error("Pipeline completed with errors.")
            st.json(context.errors)
        else:
            st.success("Pipeline completed.")
        st.json(context.results)

with tabs[3]:
    st.subheader("Runtime Scheduler")
    jobs = runtime_v3.scheduler.list_jobs()
    st.dataframe(pd.DataFrame([{"Job": k, **v} for k, v in jobs.items()]), use_container_width=True)
    if jobs:
        selected = st.selectbox("Job", list(jobs.keys()))
        if st.button("Run Job"):
            st.json(runtime_v3.scheduler.run(selected))

with tabs[4]:
    st.subheader("Event Store")
    events_context = runtime_v3.command_bus.dispatch("runtime.events", {"limit": 200})
    events = events_context.results.get("events", [])
    st.dataframe(pd.DataFrame(events), use_container_width=True)

with tabs[5]:
    st.subheader("Runtime Metrics")
    metrics_context = runtime_v3.command_bus.dispatch("runtime.metrics")
    metrics = metrics_context.results.get("metrics", [])
    st.dataframe(pd.DataFrame(metrics), use_container_width=True)

with tabs[6]:
    st.subheader("ROOST™ Founder Memory")
    st.dataframe(pd.DataFrame(runtime_v3.founder_state.recent_decisions()), use_container_width=True)
    if st.button("Create Runtime Snapshot"):
        snap_context = runtime_v3.command_bus.dispatch("runtime.snapshot")
        st.json(snap_context.results)

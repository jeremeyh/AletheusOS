import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


def safe_dataframe(data):
    """
    Converts arbitrary runtime objects into a dataframe that Streamlit
    and PyArrow can always serialize.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return df

    for col in df.columns:
        # Force every object column to clean strings
        if df[col].dtype == "object":
            df[col] = (
                df[col].apply(lambda x: "" if x is None else str(x)).astype("string")
            )

    return df


ROOT = Path(__file__).resolve().parents[1]

print("ROOT =", ROOT)
print("CWD  =", os.getcwd())
print("sys.path BEFORE")
for p in sys.path:
    print(" ", p)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print("sys.path AFTER")
for p in sys.path:
    print(" ", p)


from services.runtime_v3 import runtime_v3

st.set_page_config(
    page_title="Founder Console | CardHawkOS", page_icon="🦅", layout="wide"
)

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

tabs = st.tabs(
    [
        "Health",
        "Registry",
        "Pipeline",
        "Scheduler",
        "Events",
        "Metrics",
        "Founder Memory",
    ]
)

with tabs[0]:
    st.subheader("Runtime Health")
    st.json(health)

with tabs[1]:
    st.subheader("Runtime Registry")
    registry_context = runtime_v3.command_bus.dispatch("runtime.registry")
    registry = registry_context.results.get("registry", {})
    st.markdown("### Plugins")
    st.dataframe(safe_dataframe(registry.get("plugins", [])), width="stretch")
    st.markdown("### Commands")
    st.dataframe(
        safe_dataframe({"Command": registry.get("commands", [])}), width="stretch"
    )
    st.markdown("### Jobs")
    jobs = registry.get("jobs", {})
    st.dataframe(
        safe_dataframe([{"Job": k, **v} for k, v in jobs.items()]), width="stretch"
    )

with tabs[2]:
    st.subheader("Runtime Intelligence Pipeline")
    asset_name = st.text_input(
        "Asset / Opportunity", "Sample Caleb Williams Opportunity"
    )
    player = st.text_input("Player", "Caleb Williams")
    price = st.number_input("Price", min_value=0.0, value=150.0, step=5.0)
    serial = st.text_input("Serial", "/25")
    rookie = st.checkbox("Rookie", value=True)
    auto = st.checkbox("Autograph", value=True)
    patch = st.checkbox("Patch", value=False)

    if st.button("Run Runtime v3 Pipeline", type="primary"):
        context = runtime_v3.command_bus.dispatch(
            "runtime.pipeline",
            {
                "asset_name": asset_name,
                "player": player,
                "price": price,
                "serial": serial,
                "rookie": rookie,
                "auto": auto,
                "patch": patch,
            },
        )
        if context.errors:
            st.error("Pipeline completed with errors.")
            st.json(context.errors)
        else:
            st.success("Pipeline completed.")
        st.json(context.results)

with tabs[3]:
    st.subheader("Runtime Scheduler")
    jobs = runtime_v3.scheduler.list_jobs()
    st.dataframe(
        safe_dataframe([{"Job": k, **v} for k, v in jobs.items()]), width="stretch"
    )
    if jobs:
        selected = st.selectbox("Job", list(jobs.keys()))
        if st.button("Run Job"):
            st.json(runtime_v3.scheduler.run(selected))

with tabs[4]:
    st.subheader("Event Store")
    events_context = runtime_v3.command_bus.dispatch("runtime.events", {"limit": 200})
    events = events_context.results.get("events", [])
    st.dataframe(safe_dataframe(events), width="stretch")

with tabs[5]:
    st.subheader("Runtime Metrics")
    metrics_context = runtime_v3.command_bus.dispatch("runtime.metrics")
    metrics = metrics_context.results.get("metrics", [])
    st.dataframe(safe_dataframe(metrics), width="stretch")

with tabs[6]:
    st.subheader("ROOST™ Founder Memory")
    st.dataframe(
        safe_dataframe(runtime_v3.founder_state.recent_decisions()), width="stretch"
    )
    if st.button("Create Runtime Snapshot"):
        snap_context = runtime_v3.command_bus.dispatch("runtime.snapshot")
        st.json(snap_context.results)

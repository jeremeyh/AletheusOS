import streamlit as st

from kernel.runtime import kernel
from core.engine_registry import engine_registry
from intelligence.projections.manager import projection_manager
from core.event_bus import event_bus

st.set_page_config(page_title="Platform", layout="wide")

kernel.boot()

st.title("⚙️ CardHawk OS™ Runtime")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Engines",len(engine_registry.all()))
c2.metric("Projections",len(projection_manager.projections))
c3.metric("Listeners",sum(event_bus.listeners().values()))
c4.metric("Services",kernel.status()["services"])

st.divider()

st.subheader("Registered Engines")

for engine in engine_registry.all().keys():
    st.write("✅",engine)

st.divider()

st.subheader("Event Listeners")

st.json(event_bus.listeners())

import json
from pathlib import Path

LOG=Path("logs/events.jsonl")

st.divider()

st.subheader("Recent Events")

if LOG.exists():

    with LOG.open() as fp:

        rows=fp.readlines()[-20:]

    for row in reversed(rows):

        st.code(row.strip())

else:

    st.info("No events logged.")

TIMELINE=Path("data/timeline.json")

st.divider()

st.subheader("Timeline")

if TIMELINE.exists():

    with TIMELINE.open() as fp:

        rows=json.load(fp)

    for item in reversed(rows[-10:]):

        st.write(item["event"])

else:

    st.info("Timeline empty.")

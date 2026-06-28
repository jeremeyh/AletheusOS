import streamlit as st

from command_center.runtime.snapshot import snapshot

st.set_page_config(layout="wide")

state = snapshot()

st.title("🛰 CardHawk Command Center™")

c1,c2,c3,c4 = st.columns(4)

c1.metric("Engines", len(state["engines"]))
c2.metric("Services", len(state["services"]))
c3.metric("Projections", len(state["projections"]))
c4.metric("Listeners", sum(state["listeners"].values()))

st.divider()

left,right = st.columns([2,1])

with left:

    st.subheader("Registered Engines")

    st.dataframe(
        [{"Engine":e} for e in state["engines"]],
        use_container_width=True
    )

with right:

    st.subheader("Registered Projections")

    if state["projections"]:
        st.write(state["projections"])
    else:
        st.info("No projections registered.")

st.divider()

st.subheader("Event Listeners")

st.json(state["listeners"])

from analytics.runtime.event_metrics import metrics

st.divider()

st.subheader("Event Throughput")

st.bar_chart(metrics())

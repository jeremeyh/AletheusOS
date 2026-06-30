import streamlit as st


def render_orchestrator_run(run):
    with st.container(border=True):
        st.subheader(
            f"Run #{run.get('id')} — Asset {run.get('asset_id')}"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Status", run.get("status", "UNKNOWN"))

        with c2:
            st.metric("Steps", run.get("steps", 0))

        with c3:
            st.metric("Errors", run.get("errors", 0))

        with c4:
            st.metric("Duration", f"{float(run.get('duration') or 0):.2f}s")

        st.caption(run.get("created_at", ""))

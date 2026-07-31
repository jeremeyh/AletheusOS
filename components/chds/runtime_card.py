import streamlit as st


def runtime_card(
    title,
    value,
    status="ONLINE",
):
    """
    Runtime status card.
    """

    with st.container(border=True):
        st.caption(title)

        st.markdown(f"## {value}")

        if status == "ONLINE":
            st.success("🟢 ONLINE")

        elif status == "READY":
            st.success("🟢 READY")

        elif status == "WARNING":
            st.warning("🟡 WARNING")

        else:
            st.error("🔴 OFFLINE")

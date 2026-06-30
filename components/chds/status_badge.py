import streamlit as st


def status_badge(
    status,
):
    """
    Standard runtime badge.
    """

    status = status.upper()

    if status == "ONLINE":

        st.success("🟢 ONLINE")

    elif status == "READY":

        st.success("🟢 READY")

    elif status == "WARNING":

        st.warning("🟡 WARNING")

    else:

        st.error("🔴 OFFLINE")

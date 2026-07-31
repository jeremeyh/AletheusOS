import streamlit as st


def render_intelligence_panel(
    title,
    body,
    icon="🧠",
    status="ONLINE",
):
    """
    CardHawk Design System™

    Standard Intelligence Panel
    """

    with st.container(border=True):
        left, right = st.columns([5, 1])

        with left:
            st.subheader(f"{icon} {title}")

        with right:
            if status == "ONLINE":
                st.success("●")

            elif status == "WARNING":
                st.warning("●")

            else:
                st.error("●")

        st.write(body)

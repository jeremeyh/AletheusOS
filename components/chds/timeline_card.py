import streamlit as st


def render_timeline(
    events,
):
    """
    CardHawk Design System™

    Timeline component.
    """

    with st.container(border=True):

        st.subheader("📜 Timeline™")

        if not events:

            st.info(
                "No events."
            )

            return

        for event in events:

            st.write(
                f"• {event}"
            )

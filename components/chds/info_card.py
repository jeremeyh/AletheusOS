import streamlit as st


def render_info_card(
    title,
    body,
    icon="ℹ️",
):
    """
    CardHawk Design System™

    Generic information card.
    """

    with st.container(border=True):

        st.subheader(
            f"{icon} {title}"
        )

        st.write(body)

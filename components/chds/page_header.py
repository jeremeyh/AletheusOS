import streamlit as st


def render_page_header(
    title,
    subtitle="",
):
    """
    CardHawk Design System™

    Standard page header.
    """

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()

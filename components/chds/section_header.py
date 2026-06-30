import streamlit as st


def section_header(
    title,
    subtitle=None,
):
    """
    Standard CardHawkOS section header.
    """

    st.markdown(f"## {title}")

    if subtitle:

        st.caption(subtitle)

    st.divider()

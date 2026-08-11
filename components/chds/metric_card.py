import streamlit as st


def metric_card(
    title,
    value,
    delta=None,
    help_text=None,
):
    """
    CardHawk Design System™

    Standard metric card used throughout
    CardHawkOS.
    """

    with st.container(border=True):
        st.caption(title)

        st.markdown(f"## {value}")

        if delta is not None:
            st.success(delta)

        if help_text:
            st.caption(help_text)

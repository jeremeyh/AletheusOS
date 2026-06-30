import streamlit as st


def render_chart_card(
    title,
    dataframe,
):
    """
    CardHawk Design System™

    Standard chart container.
    """

    with st.container(border=True):

        st.subheader(title)

        st.line_chart(
            dataframe,
            width="stretch",
        )

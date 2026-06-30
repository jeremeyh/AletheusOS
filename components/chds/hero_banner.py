import streamlit as st


def render_hero(
    title,
    subtitle,
):
    """
    CardHawkOS Hero Banner
    """

    st.markdown(
        f"""
# {title}

{subtitle}
"""
    )

    st.divider()

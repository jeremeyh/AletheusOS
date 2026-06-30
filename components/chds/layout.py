import streamlit as st


def render_page_header(title, subtitle=""):
    st.markdown(
        f"""
        <div style="padding: 0.75rem 0 1.25rem 0;">
            <h1 style="margin-bottom: 0.15rem;">{title}</h1>
            <p style="color: #9ca3af; font-size: 1rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section(title, subtitle=""):
    st.markdown(f"### {title}")

    if subtitle:
        st.caption(subtitle)


def render_divider():
    st.divider()

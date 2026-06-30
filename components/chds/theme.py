import streamlit as st


CARDHAWK = {
    "primary": "#F5A623",
    "secondary": "#1F2937",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "background": "#0F172A",
    "surface": "#1E293B",
    "text": "#F8FAFC",
}


def inject_theme():
    st.markdown(
        f"""
        <style>
        :root {{
            --ch-primary: {CARDHAWK["primary"]};
            --ch-secondary: {CARDHAWK["secondary"]};
            --ch-success: {CARDHAWK["success"]};
            --ch-warning: {CARDHAWK["warning"]};
            --ch-danger: {CARDHAWK["danger"]};
        }}

        .block-container {{
            padding-top: 1rem;
        }}

        div[data-testid="stMetric"] {{
            border-radius: 12px;
            padding: 12px;
            border: 1px solid #333;
        }}

        section[data-testid="stSidebarNav"] {{
            display: none;
        }}

        footer {{
            visibility: hidden;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        header {{
            visibility: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

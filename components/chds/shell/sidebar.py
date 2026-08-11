from pathlib import Path

import streamlit as st


def load_theme():
    css = Path("assets/css/cardhawk.css")

    if css.exists():
        st.markdown(
            f"<style>{css.read_text()}</style>",
            unsafe_allow_html=True,
        )


def safe_page_link(page, label, icon):
    if Path(page).exists():
        st.page_link(
            page,
            label=label,
            icon=icon,
        )


def render_sidebar():
    load_theme()

    with st.sidebar:
        st.markdown(
            """
# 🦅 CardHawk OS™

**Collectible Intelligence Platform**
"""
        )

        st.caption("v1.0 Developer Preview")

        st.divider()

        st.markdown("### Home")
        st.page_link("app.py", label="Home", icon="🏠")

        st.divider()

        st.markdown("### Asset Workflow")

        safe_page_link("pages/01_Asset_Intake.py", label="Intake Wizard™", icon="📥")
        safe_page_link("pages/05_Intake_Wizard.py", label="Scan & Review™", icon="📷")
        safe_page_link("pages/03_Asset_Explorer.py", label="Asset Vault™", icon="🗂")
        safe_page_link(
            "pages/04_Asset_Intelligence.py", label="Asset Intelligence™", icon="🧬"
        )
        safe_page_link("pages/06_Asset_Detail.py", label="Asset Detail™", icon="🔍")
        safe_page_link(
            "pages/08_Intelligence_Workspace.py",
            label="Intelligence Workspace™",
            icon="🧠",
        )

        st.divider()

        st.markdown("### Intelligence")

        safe_page_link(
            "pages/07_Mission_Control.py", label="Mission Control™", icon="📊"
        )
        safe_page_link(
            "pages/09_Marketplace_Intelligence.py",
            label="Marketplace Intelligence™",
            icon="💰",
        )
        safe_page_link(
            "pages/10_DEF_Command_Center.py", label="DEF Command Center™", icon="🎯"
        )
        safe_page_link(
            "pages/11_NEST_Intelligence.py", label="NEST™ Intelligence", icon="🪺"
        )
        safe_page_link(
            "pages/12_FALCON_Command_Center.py",
            label="FALCON™ Command Center",
            icon="🦅",
        )
        safe_page_link("pages/13_ORCHESTRATOR.py", label="ORCHESTRATOR™", icon="🛰")
        safe_page_link(
            "pages/98_Command_Center.py", label="Founder Copilot™", icon="🧠"
        )
        safe_page_link("pages/98_Command_Center.py", label="THORᵡ™", icon="⚡")

        st.divider()

        st.markdown("### Platform")

        safe_page_link("pages/99_Platform.py", label="Platform™", icon="⚙")
        safe_page_link(
            "pages/enterprise_diagnostics.py", label="Diagnostics", icon="🔧"
        )

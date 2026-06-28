import streamlit as st
from services.live_platform_service import LivePlatformService
from components.live_platform_ui import hero, founder_brief, panel, asset_rows, marketplace_rows, action_rows

def render(state):
    data = LivePlatformService.dashboard(state)
    hero()
    st.title("🦅 Founder Workspace™")

    left, right = st.columns([1.1,1])
    with left:
        founder_brief(data["brief"])
    with right:
        panel("Daily Actions™", action_rows(data["actions"]))

    st.divider()

    c1,c2,c3 = st.columns(3)
    with c1:
        panel("Scout™", marketplace_rows(data["marketplace"]))
    with c2:
        panel("THORᵡ™", asset_rows(data["ranked"], "thorx", 6))
    with c3:
        panel("DEX™ / DEF™", [("Offer Strategy", "<span class='ch-pill'>Ready</span>", "Use Negotiation Center"), ("Capital Allocation", "<span class='ch-pill'>Ready</span>", "Use Autonomous Intelligence")])

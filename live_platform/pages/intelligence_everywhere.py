import streamlit as st
from services.live_platform_service import LivePlatformService
from components.live_platform_ui import hero, panel

def render(state):
    data = LivePlatformService.dashboard(state)
    hero()
    st.title("🧠 Intelligence Everywhere™")

    recommendations = []
    if data["strike"]:
        recommendations.append(("Review Strike Zone™", "<span class='ch-pill'>Now</span>", "Actionable alert exists"))
    if data["ranked"]:
        recommendations.append(("Reprice THORᵡ leader", "<span class='ch-pill'>Today</span>", "Highest conviction needs current market check"))
    recommendations.append(("Run Scout™", "<span class='ch-pill'>Daily</span>", "Find new opportunities"))
    recommendations.append(("Simulate acquisition", "<span class='ch-pill'>Before bid</span>", "Protect portfolio fit"))

    panel("Recommendations™", recommendations)

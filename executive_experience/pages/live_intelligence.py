import streamlit as st
from services.executive_experience_service import ExecutiveExperienceService
from components.executive_ui import hero, panel, activity_rows, task_rows

def render(state):
    data = ExecutiveExperienceService.build_dashboard(state)
    hero()
    st.title("🧠 Live Intelligence Layer™")

    c1,c2 = st.columns(2)
    with c1:
        panel("Activity Feed™", activity_rows(data["activity"]))
    with c2:
        panel("Recommendations™", task_rows(data["tasks"]))

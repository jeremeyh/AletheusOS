import streamlit as st
from components.executive_ui import activity_rows, hero, panel, task_rows
from services.executive_experience_service import ExecutiveExperienceService


def render(state):
    data = ExecutiveExperienceService.build_dashboard(state)
    hero()
    st.title("🧠 Live Intelligence Layer™")

    c1,c2 = st.columns(2)
    with c1:
        panel("Activity Feed™", activity_rows(data["activity"]))
    with c2:
        panel("Recommendations™", task_rows(data["tasks"]))

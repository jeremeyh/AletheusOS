import streamlit as st
from workflow_automation.workflow_service import WorkflowAutomationService

def render(state):
    st.title("🔁 Workflow Automation™")
    st.caption("Asset Intake • Acquisition • Exit")

    c1, c2 = st.columns([1, 2])
    with c1:
        workflow_type = st.selectbox("Workflow", list(WorkflowAutomationService.TEMPLATES.keys()))
        subject = st.text_input("Subject / Asset / Listing")
        if st.button("Start Workflow"):
            WorkflowAutomationService.start(workflow_type, subject)
            st.success("Workflow started.")

    with c2:
        st.subheader("Workflow Templates")
        st.json(WorkflowAutomationService.TEMPLATES)

    st.divider()
    st.subheader("Active Runs")
    for run in WorkflowAutomationService.all():
        with st.container(border=True):
            st.write(f"**{run.workflow_type}** — {run.subject}")
            st.caption(f"{run.run_id} • {run.status}")
            for step in run.steps:
                st.write(f"{'✅' if step.status == 'complete' else '⬜'} {step.name}")
            if st.button("Advance", key=run.run_id):
                WorkflowAutomationService.advance(run.run_id)
                st.rerun()

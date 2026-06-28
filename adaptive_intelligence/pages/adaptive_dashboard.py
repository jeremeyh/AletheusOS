import streamlit as st
from adaptive_intelligence.adaptive_service import AdaptiveIntelligenceService
from components.adaptive_ui import adaptive_hero, status_panel

def render(state):
    adaptive_hero()
    st.title("🧠 CardHawk OS™ 7.0 — Adaptive Intelligence™")

    tabs = st.tabs([
        "7A Feedback Loop",
        "7B Explainability",
        "7C Simulation Lab",
        "7D Quality Dashboard",
        "7E Research Workspace",
        "7F Plugins",
        "7G Deployment Profiles",
        "7H Governance",
    ])

    with tabs[0]:
        st.subheader("Intelligence Feedback Loop™")
        rec_type = st.selectbox("Recommendation Type", ["Buy", "Sell", "Grade", "Watch", "Pass"])
        subject = st.text_input("Subject", "Caleb Williams Gold /10")
        recommendation = st.text_input("Recommendation", "BUY")
        accepted = st.selectbox("Accepted?", ["Unknown", "Yes", "No"])
        predicted = st.number_input("Predicted Value", 0.0, value=250.0)
        actual = st.number_input("Actual Value", 0.0, value=0.0)
        notes = st.text_area("Notes")
        if st.button("Record Feedback"):
            AdaptiveIntelligenceService.feedback.record(
                rec_type, subject, recommendation,
                None if accepted == "Unknown" else accepted == "Yes",
                predicted, actual, notes=notes,
            )
            st.success("Feedback recorded.")
        status_panel("Feedback Metrics", AdaptiveIntelligenceService.feedback.metrics())

    with tabs[1]:
        st.subheader("Explainable Intelligence™")
        sample = {
            "thorx_score": 9.2,
            "components": {
                "scarcity": 9.5,
                "player_thesis": 9.0,
                "portfolio_fit": 8.8,
                "risk": 6.9,
                "liquidity": 7.5,
            }
        }
        status_panel("Sample THORᵡ Explanation", AdaptiveIntelligenceService.explainer.explain_thorx(sample))

    with tabs[2]:
        st.subheader("Portfolio Simulation Lab™")
        raw = st.number_input("Raw Value", 0.0, value=150.0)
        grading_cost = st.number_input("Grading Cost", 0.0, value=35.0)
        gem = st.number_input("Gem Value", 0.0, value=375.0)
        prob = st.slider("Gem Probability", 0.0, 1.0, 0.45)
        status_panel("Grade vs Raw", AdaptiveIntelligenceService.simulation.grade_vs_raw(raw, grading_cost, gem, prob))

    with tabs[3]:
        status_panel("Intelligence Quality Dashboard™", AdaptiveIntelligenceService.quality.snapshot())

    with tabs[4]:
        st.subheader("Research Workspace™")
        AdaptiveIntelligenceService.research.seed()
        research_type = st.selectbox("Research Type", ["Player Dossier", "Market Report", "Set Analysis", "Parallel Study", "Population Trend", "Thesis Revision"])
        title = st.text_input("Research Title")
        body = st.text_area("Research Body")
        if st.button("Save Research"):
            AdaptiveIntelligenceService.research.create(research_type, title, body)
            st.success("Research saved.")
        for note in AdaptiveIntelligenceService.research.all(research_type):
            with st.container(border=True):
                st.write(f"**{note.title}**")
                st.caption(note.created_at)
                st.write(note.body)

    with tabs[5]:
        status_panel("Plugin Registry™", [p.__dict__ for p in AdaptiveIntelligenceService.plugins.seed_defaults()])

    with tabs[6]:
        status_panel("Deployment Profiles™", AdaptiveIntelligenceService.deployment.all())

    with tabs[7]:
        status_panel("Platform Governance™", AdaptiveIntelligenceService.governance.validate())
        status_panel("Compatibility Report", AdaptiveIntelligenceService.governance.compatibility_report())

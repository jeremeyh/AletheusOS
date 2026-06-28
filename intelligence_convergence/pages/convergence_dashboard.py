import streamlit as st
from services.intelligence_convergence_service import IntelligenceConvergenceService
from components.convergence_ui import convergence_hero, decision_panel, commercial_checklist

def render(state):
    convergence_hero()
    st.title("🧠 Alpha 5.0 — Intelligence Convergence™")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Unified Intelligence™",
        "Acquisition AI™",
        "Exit Intelligence™",
        "Digital Twin 2.0™",
        "Knowledge Graph™",
    ])

    engine = IntelligenceConvergenceService.engine(state)

    with tab1:
        st.subheader("Candidate Decision Pipeline")
        title = st.text_input("Candidate Title", "Caleb Williams Gold /10 Rookie")
        price = st.number_input("Price", 0.0, value=250.0)
        estimated_value = st.number_input("Estimated Value", 0.0, value=425.0)
        scout_score = st.slider("Scout / THORᵡ Proxy", 0.0, 10.0, 9.4)
        ni = st.slider("NI™", 0.0, 5.0, 4.5)
        if st.button("Run Unified Intelligence"):
            result = engine.analyze_candidate({
                "title": title,
                "price": price,
                "estimated_value": estimated_value,
                "scout_score": scout_score,
                "thorx_score": scout_score,
                "ni_score": ni,
            })
            st.session_state["convergence_result"] = result
        if "convergence_result" in st.session_state:
            decision_panel(st.session_state["convergence_result"])
            st.json(st.session_state["convergence_result"])

    with tab2:
        st.info("Acquisition AI evaluates purchase price, upside, capital impact, and alternatives.")

    with tab3:
        st.info("Exit Intelligence recommends hold, sell, grade, auction, consign, vault, trade, or bundle.")

    with tab4:
        assets = []
        svc = state["container"].service("assets")
        if svc:
            try: assets = svc.get_all()
            except Exception: assets = []
        scenario = st.selectbox("Scenario", ["Base Case", "Player MVP", "PSA 10 Grade", "Championship Run", "Market Pullback", "Injury / Thesis Break"])
        st.json(engine.simulate_future(assets, scenario))

    with tab5:
        assets = []
        svc = state["container"].service("assets")
        if svc:
            try: assets = svc.get_all()
            except Exception: assets = []
        st.json(IntelligenceConvergenceService.build_knowledge_graph(assets))

    st.divider()
    commercial_checklist(IntelligenceConvergenceService.commercial_status())

import streamlit as st
from services.live_data_activation_service import LiveDataActivationService
from components.live_data_ui import render_listing_cards, render_comp_summary

def render(state):
    st.title("🌐 Live Data Activation™")
    st.caption("Provider-ready marketplace search, comps, watchlist scanning, and value bands.")

    tab1, tab2, tab3 = st.tabs(["Search", "Comps", "Watchlist"])

    with tab1:
        query = st.text_input("Search Query", "Caleb Williams Gold /10", key="live_search")
        if st.button("Run Live Search"):
            listings = LiveDataActivationService.search(query)
            st.session_state["live_search_results"] = listings
        render_listing_cards(st.session_state.get("live_search_results", []))

    with tab2:
        comp_query = st.text_input("Comp Query", "Caleb Williams Gold /10", key="comp_query")
        if st.button("Build Comps"):
            st.session_state["comp_result"] = LiveDataActivationService.comps(comp_query)
        if "comp_result" in st.session_state:
            render_comp_summary(st.session_state["comp_result"])
            render_listing_cards([type("Obj", (), x) for x in st.session_state["comp_result"].get("listings", [])])

    with tab3:
        watch_query = st.text_input("Watch Query", "Rome Odunze RPA /25")
        max_price = st.number_input("Max Price", 0.0, value=150.0)
        min_score = st.slider("Min Score", 0.0, 10.0, 8.0)
        if st.button("Add Watch Target"):
            LiveDataActivationService.watch(watch_query, max_price, min_score)
            st.success("Watch target added.")

        if st.button("Scan Watchlist"):
            st.session_state["watch_scan"] = LiveDataActivationService.scan_watchlist()

        st.json(st.session_state.get("watch_scan", {}))

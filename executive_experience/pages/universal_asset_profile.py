import streamlit as st
from services.executive_experience_service import ExecutiveExperienceService
from components.executive_ui import hero
from components.cardhawk_utils import row_value, safe_float, roi_percent, money

def render(state):
    assets = ExecutiveExperienceService.get_assets(state)
    hero()
    st.title("🧬 Universal Asset Profile™")

    if not assets:
        st.info("No assets available.")
        return

    labels = [f"{row_value(a,'asset_id','')} — {row_value(a,'player','Unknown')} — {row_value(a,'brand','')}" for a in assets]
    choice = st.selectbox("Asset", labels)
    asset = assets[labels.index(choice)]

    st.markdown(f"## {row_value(asset,'player','Unknown Asset')}")
    st.caption(f"{row_value(asset,'year','')} {row_value(asset,'brand','')} • {row_value(asset,'set_name','')} • {row_value(asset,'parallel','')}")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("THORᵡ", f"{safe_float(row_value(asset,'thorx_score',0)):.1f}")
    c2.metric("Value", money(row_value(asset,"current_value",0)))
    c3.metric("Cost", money(row_value(asset,"purchase_price",0)))
    c4.metric("ROI", f"{roi_percent(row_value(asset,'purchase_price',0), row_value(asset,'current_value',0)):.1f}%")
    c5.metric("NI™", f"{safe_float(row_value(asset,'ni_score',0)):.1f}")

    tabs = st.tabs(["Hero Image", "Asset DNA™", "Genome™", "THORᵡ Breakdown", "Hawk A•Eye™", "Marketplace", "Exit Strategy", "Digital Twin™", "Founder Notes"])
    with tabs[0]:
        st.info("Large image hero staged.")
    with tabs[1]:
        st.json({k: row_value(asset,k,"") for k in ["player","team","sport","category","year","brand","set_name","parallel","serial_number","print_run","grade"]})
    with tabs[2]:
        st.info("Ownership and lifecycle timeline staged.")
    with tabs[3]:
        st.write("Classification:", row_value(asset,"classification",""))
        st.write("Recommendation:", row_value(asset,"recommendation",""))
    with tabs[4]:
        st.info("Vision/OCR results staged.")
    with tabs[5]:
        st.info("Comps and pricing history staged.")
    with tabs[6]:
        try:
            from exit_strategy.exit_strategy_service import ExitStrategyService
            st.json(ExitStrategyService.recommend(asset))
        except Exception:
            st.info("Exit Strategy™ staged.")
    with tabs[7]:
        st.info("Digital Twin™ scenario modeling staged.")
    with tabs[8]:
        st.write(row_value(asset,"notes","No notes recorded."))

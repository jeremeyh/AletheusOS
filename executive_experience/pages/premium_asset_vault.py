import streamlit as st
from components.executive_ui import hero
from services.executive_experience_service import ExecutiveExperienceService

from components.cardhawk_utils import money, roi_percent, row_value, safe_float


def render(state):
    assets = ExecutiveExperienceService.get_assets(state)
    hero()
    st.title("📦 Premium Asset Vault™")

    c1, c2, c3 = st.columns([2, 1, 1])
    query = c1.text_input("Search", placeholder="Player, brand, set, parallel, serial, notes...")
    min_thorx = c2.slider("Min THORᵡ", 0.0, 10.0, 0.0, 0.1)
    view = c3.selectbox("View", ["Cards", "Data Grid"])

    filtered = []
    for a in assets:
        hay = " ".join(str(row_value(a,k,"")) for k in ["player","team","sport","brand","set_name","parallel","serial_number","notes"]).lower()
        if query and query.lower() not in hay:
            continue
        if safe_float(row_value(a,"thorx_score",0)) < min_thorx:
            continue
        filtered.append(a)

    st.caption(f"{len(filtered)} of {len(assets)} assets")

    if view == "Data Grid":
        st.dataframe(filtered, use_container_width=True)
    else:
        for asset in filtered:
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3,1,1,1])
                c1.markdown(f"### {row_value(asset,'player','Unknown Asset')}")
                c1.caption(f"{row_value(asset,'year','')} {row_value(asset,'brand','')} • {row_value(asset,'set_name','')} • {row_value(asset,'parallel','')}")
                c2.metric("THORᵡ", f"{safe_float(row_value(asset,'thorx_score',0)):.1f}")
                c3.metric("Value", money(row_value(asset,"current_value",0)))
                c4.metric("ROI", f"{roi_percent(row_value(asset,'purchase_price',0), row_value(asset,'current_value',0)):.1f}%")

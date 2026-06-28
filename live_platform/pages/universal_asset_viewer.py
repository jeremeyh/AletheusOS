import streamlit as st
from services.live_platform_service import LivePlatformService
from components.cardhawk_utils import row_value, safe_float, roi_percent, money
from components.live_platform_ui import hero

def render(state):
    assets = LivePlatformService.assets(state)
    hero()
    st.title("🧬 Universal Asset Viewer™")

    if not assets:
        st.info("No assets available.")
        return

    labels = [f"{row_value(a,'asset_id','')} — {row_value(a,'player','Unknown')} — {row_value(a,'brand','')}" for a in assets]
    choice = st.selectbox("Select Asset", labels)
    asset = assets[labels.index(choice)]

    st.markdown(f"## {row_value(asset,'player','Unknown Asset')}")
    st.caption(f"{row_value(asset,'year','')} {row_value(asset,'brand','')} • {row_value(asset,'set_name','')} • {row_value(asset,'parallel','')}")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("THORᵡ", f"{safe_float(row_value(asset,'thorx_score',0)):.1f}")
    c2.metric("Value", money(row_value(asset,'current_value',0)))
    c3.metric("Cost", money(row_value(asset,'purchase_price',0)))
    c4.metric("ROI", f"{roi_percent(row_value(asset,'purchase_price',0), row_value(asset,'current_value',0)):.1f}%")
    c5.metric("NI™", f"{safe_float(row_value(asset,'ni_score',0)):.1f}")

    tabs = st.tabs(["Images", "Asset DNA™", "Genome™", "THORᵡ™", "Marketplace™", "Timeline™", "Founder Notes™"])
    with tabs[0]:
        img = row_value(asset, "front_image", "") or row_value(asset, "image_path", "")
        if img:
            try: st.image(img, width=420)
            except Exception: st.info("Image path stored but not displayable.")
        else:
            st.info("No image stored.")
    with tabs[1]:
        st.json({k: row_value(asset,k,"") for k in ["player","team","sport","category","year","brand","set_name","parallel","serial_number","print_run","grade"]})
    with tabs[2]:
        st.info("Genome lifecycle memory staged.")
    with tabs[3]:
        st.write("THORᵡ:", row_value(asset,"thorx_score",0))
        st.write("Classification:", row_value(asset,"classification",""))
        st.write("Recommendation:", row_value(asset,"recommendation",""))
    with tabs[4]:
        st.info("Normalized marketplace comps and opportunities will display here.")
    with tabs[5]:
        st.info("Timeline events will display here.")
    with tabs[6]:
        st.write(row_value(asset,"notes","No notes recorded."))

import streamlit as st

from asset_core.runtime.image_service import AssetImageService


def render_asset_card(asset):
    image = AssetImageService.get_image(asset)

    player = asset.get("player") or "Unknown"
    brand = asset.get("brand") or ""
    set_name = asset.get("set_name") or ""
    value = float(asset.get("current_value") or 0)
    thorx = float(asset.get("thorx_score") or 0)
    grade = asset.get("grade") or "Raw"

    with st.container(border=True):
        st.image(image, width="stretch")

        st.subheader(player)
        st.caption(f"{brand} • {set_name}")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Market", f"${value:,.2f}")

        with c2:
            st.metric("THORᵡ", f"{thorx:.1f}")

        st.progress(max(0.0, min(thorx / 100.0, 1.0)))
        st.caption(f"Condition: {grade}")

        st.button(
            "Open Intelligence Workspace",
            key=f"asset_{asset.get('id', player)}",
            width="stretch",
        )


asset_card = render_asset_card

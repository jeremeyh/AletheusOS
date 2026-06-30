import streamlit as st

from components.chds.asset_card import render_asset_card


def render_asset_gallery(assets, columns=3, limit=6):
    st.subheader("🖼 Portfolio Gallery")

    if not assets:
        st.info("No assets available.")
        return

    visible_assets = assets[:limit]
    grid = st.columns(columns)

    for index, asset in enumerate(visible_assets):
        with grid[index % columns]:
            render_asset_card(asset)


asset_gallery = render_asset_gallery

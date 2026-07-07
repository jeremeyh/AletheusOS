import streamlit as st

from asset_core.runtime.image_service import AssetImageService
from components.chds.asset_card import render_asset_card


def render_asset_gallery(assets, columns=3, limit=6):
    st.subheader("🖼 Portfolio Gallery")

    if not assets:
        st.info("No assets available.")
        return

    #
    # Prefer assets with real images.
    #
    with_images = [
        asset
        for asset in assets
        if AssetImageService.has_real_image(asset)
    ]

    without_images = [
        asset
        for asset in assets
        if not AssetImageService.has_real_image(asset)
    ]

    visible_assets = (with_images + without_images)[:limit]

    grid = st.columns(columns)

    for index, asset in enumerate(visible_assets):
        with grid[index % columns]:
            render_asset_card(asset)


asset_gallery = render_asset_gallery

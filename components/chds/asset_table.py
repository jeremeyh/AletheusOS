import pandas as pd
import streamlit as st


def render_asset_table(snapshot):
    """
    CardHawkOS Professional Asset Vault™
    """

    assets = snapshot.get("top_assets", [])

    if not assets:
        st.info("No assets available.")
        return

    rows = []

    for asset in assets:
        purchase = asset.get("purchase_price") or 0
        value = asset.get("current_value") or 0

        roi = 0

        if purchase:
            roi = ((value - purchase) / purchase) * 100

        rows.append(
            {
                "Player": asset.get("player"),
                "Brand": asset.get("brand"),
                "Set": asset.get("set_name"),
                "Value": value,
                "THORᵡ": round(asset.get("thorx_score", 0), 1),
                "ROI %": round(roi, 2),
            }
        )

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        width="stretch",
        height=420,
        hide_index=True,
    )

import sqlite3
from pathlib import Path

import streamlit as st

DB = "data/cardhawk.db"

st.set_page_config(
    page_title="Asset Intelligence™",
    page_icon="🦅",
    layout="wide",
)

st.title("🦅 Asset Intelligence™")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

rows = conn.execute("""
SELECT *
FROM assets
ORDER BY player, id
""").fetchall()

conn.close()

if not rows:
    st.info("No assets found.")
    st.stop()

lookup = {
    f"{r['id']} — {r['player']}": dict(r)
    for r in rows
}

selected = st.selectbox(
    "Select Asset",
    lookup.keys(),
)

asset = lookup[selected]

st.divider()

img_col, info_col = st.columns([1, 2])

with img_col:

    st.subheader("Images")

    front = asset.get("front_image")
    back = asset.get("back_image")

    if front and Path(front).exists():
        st.image(front, use_container_width=True)
    else:
        st.info("No front image.")

    if back and Path(back).exists():
        st.image(back, use_container_width=True)

with info_col:

    st.subheader("Asset DNA™")

    c1, c2 = st.columns(2)

    with c1:
        st.write("**Player**", asset.get("player"))
        st.write("**Brand**", asset.get("brand"))
        st.write("**Set**", asset.get("set_name"))
        st.write("**Parallel**", asset.get("parallel"))

    with c2:
        st.write("**Grade**", asset.get("grade"))
        st.write("**Autograph**", "Yes" if asset.get("autograph") else "No")
        st.write("**Patch**", "Yes" if asset.get("patch") else "No")
        st.write("**THORᵡ**", asset.get("thorx_score"))

st.divider()

m1, m2, m3 = st.columns(3)

m1.metric(
    "Current Value",
    f"${float(asset.get('current_value') or 0):,.2f}"
)

m2.metric(
    "Purchase",
    f"${float(asset.get('purchase_price') or 0):,.2f}"
)

gain = (
    float(asset.get("current_value") or 0)
    - float(asset.get("purchase_price") or 0)
)

m3.metric(
    "Gain / Loss",
    f"${gain:,.2f}"
)

st.divider()

st.subheader("Founder AI™")

score = float(asset.get("thorx_score") or 0)

if score >= 95:
    st.success("🟢 Elite long-term asset.")
elif score >= 85:
    st.success("🟢 Strong acquisition.")
elif score >= 70:
    st.warning("🟡 Hold and monitor.")
else:
    st.error("🔴 Review investment thesis.")

st.divider()

st.subheader("Asset Record")

st.json(asset)

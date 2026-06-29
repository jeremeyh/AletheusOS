import streamlit as st

from portfolio.digital_twin.engine import PortfolioDigitalTwin
from asset_core.runtime.enrichment import AssetEnrichmentEngine


st.set_page_config(
    page_title="CardHawk Mission Control™",
    page_icon="🦅",
    layout="wide",
)

st.title("🦅 CardHawk Mission Control™")
st.caption("Portfolio intelligence, asset enrichment, and operating system status.")

col1, col2, col3, col4 = st.columns(4)

snapshot = PortfolioDigitalTwin.snapshot()

with col1:
    st.metric(
        "Portfolio Value",
        f"${snapshot['total_value']:,.2f}",
    )

with col2:
    st.metric(
        "Gain / Loss",
        f"${snapshot['gain_loss']:,.2f}",
    )

with col3:
    st.metric(
        "Assets",
        snapshot["asset_count"],
    )

with col4:
    st.metric(
        "Avg THORᵡ",
        snapshot["average_thorx"],
    )

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("🏆 Top Assets")

    top_assets = snapshot.get("top_assets", [])

    if not top_assets:
        st.info("No assets found yet.")
    else:
        for asset in top_assets:
            st.markdown(
                f"""
                **#{asset.get('id')} — {asset.get('player') or 'Unknown Asset'}**  
                {asset.get('year') or ''} {asset.get('brand') or ''} {asset.get('set_name') or ''}  
                Value: **${float(asset.get('current_value') or 0):,.2f}**  
                THORᵡ: **{float(asset.get('thorx_score') or 0):.2f}**
                """
            )
            st.divider()

with right:
    st.subheader("📊 Allocation by Player")

    allocation = snapshot.get("allocation_by_player", {})

    if not allocation:
        st.info("No allocation data yet.")
    else:
        for player, value in allocation.items():
            st.write(f"**{player}**")
            st.progress(
                min(
                    1.0,
                    float(value) / max(float(snapshot["total_value"] or 1), 1),
                )
            )
            st.caption(f"${float(value):,.2f}")

st.divider()

st.subheader("🛠️ System Actions")

if st.button("Refresh Asset Intelligence"):
    count = AssetEnrichmentEngine.refresh_all()
    st.success(f"Refreshed {count} asset(s).")
    st.rerun()

st.divider()

st.subheader("🧠 Founder AI™ Daily Brief")

if snapshot["asset_count"] == 0:
    st.info("Add assets to generate a Founder AI™ brief.")
else:
    top = snapshot["top_assets"][0] if snapshot["top_assets"] else None

    if top:
        st.success(
            f"Current portfolio value is ${snapshot['total_value']:,.2f}. "
            f"Top asset is {top.get('player')} with THORᵡ "
            f"{float(top.get('thorx_score') or 0):.2f}. "
            f"Current focus: improve card-specific marketplace matching and "
            f"continue enriching high-conviction assets."
        )

st.divider()

st.subheader("📦 Raw Portfolio Snapshot")

with st.expander("View Snapshot JSON"):
    st.json(snapshot)

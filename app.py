import pandas as pd
import streamlit as st

from command_center.runtime.palette import CommandPalette
from components.chds.asset_gallery import render_asset_gallery
from components.chds.core.bootstrap import bootstrap
from components.chds.layout import render_divider, render_page_header, render_section
from components.chds.metrics import render_kpi_row
from components.chds.portfolio_health import render_portfolio_health
from components.chds.portfolio_health_card import render_portfolio_health_card
from founder_ai.copilot.engine import FounderCopilot
from portfolio.digital_twin.engine import PortfolioDigitalTwin
from portfolio.health.engine import PortfolioHealth

bootstrap(
    title="CardHawk OS™",
    icon="🦅",
)

snapshot = PortfolioDigitalTwin.snapshot()
health = PortfolioHealth.snapshot()

render_page_header(
    "🦅 CardHawk OS™",
    "Live Portfolio Intelligence Platform",
)

render_kpi_row(snapshot)

render_portfolio_health_card(health)

render_divider()

left, center, right = st.columns([1.35, 1.45, 1.2])

with left:
    render_asset_gallery(
        snapshot.get("top_assets", []),
        columns=2,
        limit=4,
    )

with center:
    render_section("📈 Portfolio Allocation")

    allocation = snapshot.get("allocation_by_player", {})

    if allocation:
        df = pd.DataFrame(
            {
                "Player": list(allocation.keys()),
                "Value": list(allocation.values()),
            }
        )

        st.bar_chart(
            df.set_index("Player"),
            width="stretch",
            height=320,
        )

    else:
        st.info("No allocation data available.")

    render_divider()

    render_portfolio_health(snapshot)

with right:
    render_section("🧠 Founder Copilot™")

    prompt = st.text_input(
        "Ask Founder Copilot",
        placeholder="portfolio, refresh portfolio, show my top assets",
    )

    if prompt:
        response = FounderCopilot.ask(prompt)
        st.json(response)

    render_divider()

    render_section("⚙ Command Palette™")

    command = st.text_input(
        "Run Command",
        placeholder="help, portfolio, refresh portfolio",
    )

    if command:
        result = CommandPalette.execute(command)
        st.json(result)

render_divider()

bottom_left, bottom_right = st.columns([1.4, 1.1])

with bottom_left:
    render_section("🏆 Highest THORᵡ Assets")

    highest = snapshot.get("highest_thorx", [])

    if highest:
        for asset in highest[:5]:
            st.write(f"**#{asset.get('id')} — {asset.get('player') or 'Unknown'}**")

            st.caption(
                f"{asset.get('brand') or ''} {asset.get('set_name') or ''} • "
                f"THORᵡ {float(asset.get('thorx_score') or 0):.1f} • "
                f"${float(asset.get('current_value') or 0):,.2f}"
            )

            st.divider()
    else:
        st.info("No THORᵡ scores available.")

with bottom_right:
    render_section("💰 Marketplace Watch")

    st.metric("Portfolio Value", f"${float(snapshot.get('total_value') or 0):,.2f}")
    st.metric("Cost Basis", f"${float(snapshot.get('total_cost') or 0):,.2f}")
    st.metric("Gain / Loss", f"${float(snapshot.get('gain_loss') or 0):,.2f}")
    st.metric("Avg THORᵡ", f"{float(snapshot.get('average_thorx') or 0):.2f}")

render_divider()

render_section("📦 Live Portfolio Snapshot")

with st.expander("View Raw Snapshot"):
    st.json(snapshot)

import streamlit as st


def render_kpi_row(snapshot):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Portfolio Value",
        f"${float(snapshot.get('total_value') or 0):,.2f}",
    )

    c2.metric(
        "Gain / Loss",
        f"${float(snapshot.get('gain_loss') or 0):,.2f}",
    )

    c3.metric(
        "Assets",
        snapshot.get("asset_count", 0),
    )

    c4.metric(
        "Avg THORᵡ",
        snapshot.get("average_thorx", 0),
    )

import streamlit as st


def render_kpi_panel(metrics):
    """
    CardHawk Design System™

    Enterprise KPI Panel
    """

    if not metrics:
        return

    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):

        with column:

            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                help=metric.get("help"),
            )

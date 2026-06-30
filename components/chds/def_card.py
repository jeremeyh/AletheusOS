import streamlit as st


def render_def_card(report):
    """
    DEF Report Card™
    """

    with st.container(border=True):
        st.subheader(
            f"{report.get('strike_zone')} #{report.get('asset_id')} — {report.get('player')}"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Final DEF", f"{float(report.get('final_score') or 0):.2f}")

        with c2:
            st.metric("Q-DEF", f"{float(report.get('qdef_score') or 0):.2f}")

        with c3:
            st.metric("D-DEF", f"{float(report.get('ddef_score') or 0):.2f}")

        with c4:
            st.metric("Confidence", f"{float(report.get('confidence') or 0):.0f}%")

        recommendation = report.get("recommendation", "WATCH")

        if recommendation in ["STRIKE", "BUY"]:
            st.success(f"Recommendation: {recommendation}")
        elif recommendation == "HOLD":
            st.info(f"Recommendation: {recommendation}")
        elif recommendation == "WATCH":
            st.warning(f"Recommendation: {recommendation}")
        else:
            st.error(f"Recommendation: {recommendation}")

        st.markdown("**Why**")

        for reason in report.get("explanation", []):
            st.write(f"• {reason}")

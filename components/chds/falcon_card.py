import streamlit as st


def render_falcon_health(health):
    st.subheader("🦅 FALCON™ Health")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Grade", health.get("collection_grade", "N/A"))

    with c2:
        st.metric("Overall", f"{float(health.get('overall') or 0):.2f}")

    with c3:
        st.metric("Quality", f"{float(health.get('investment_quality') or 0):.2f}")

    with c4:
        st.metric("Risk", f"{float(health.get('risk') or 0):.2f}")


def render_falcon_forecast(forecast):
    st.subheader("📈 FALCON™ Forecast")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Current", f"${float(forecast.get('current_value') or 0):,.2f}")

    with c2:
        st.metric("30 Day", f"${float(forecast.get('thirty_day') or 0):,.2f}")

    with c3:
        st.metric("90 Day", f"${float(forecast.get('ninety_day') or 0):,.2f}")

    with c4:
        st.metric("1 Year", f"${float(forecast.get('one_year') or 0):,.2f}")

import streamlit as st
from components.executive_ui import hero


def render(state):
    hero()
    st.title("💬 Founder AI Workspace™")
    st.caption(
        "Ask questions against your portfolio, Scout™, THORᵡ, marketplace, and Founder intelligence."
    )

    q = st.text_input("Ask Founder AI™", "What should I buy today?")
    if q:
        try:
            from founder_ai.founder_ai_service import FounderAIService

            st.success(FounderAIService.answer(q))
        except Exception:
            st.info("Founder AI is staged. Connect full reasoning engine next.")

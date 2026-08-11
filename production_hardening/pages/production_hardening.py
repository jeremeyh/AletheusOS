import streamlit as st
from production_hardening.hardening_service import ProductionHardeningService


def render(state):
    st.title("🛡️ Production Hardening™")
    st.json(ProductionHardeningService.checklist())

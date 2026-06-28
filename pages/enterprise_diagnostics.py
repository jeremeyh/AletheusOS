import streamlit as st
from diagnostics.enterprise_diagnostics import EnterpriseDiagnostics

try:
    from themes.cardhawk_theme import apply_cardhawk_theme, render_sidebar_brand
    apply_cardhawk_theme()
    render_sidebar_brand()
except Exception:
    pass

st.set_page_config(page_title="Enterprise Diagnostics™ | CardHawk OS™", page_icon="🧪", layout="wide")

st.title("🧪 Enterprise Diagnostics™")
st.caption("Alpha 2.3D — Production Engineering")

if st.button("Run Enterprise Diagnostics"):
    st.session_state["enterprise_diagnostics"] = EnterpriseDiagnostics.run()

if "enterprise_diagnostics" in st.session_state:
    st.json(st.session_state["enterprise_diagnostics"])
else:
    st.info("Run diagnostics to verify production engineering systems.")

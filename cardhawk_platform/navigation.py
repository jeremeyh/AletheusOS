import streamlit as st

NAV_GROUPS = {
    "Founder™": [
        ("Dashboard", "dashboard", "🦅"),
        ("Command Center", "command_center", "🎛️"),
        ("Founder Workspace", "founder_workspace", "🧠"),
        ("Founder Studio", "founder_studio", "🏛️"),
        ("Founder AI", "founder_ai", "💬"),
    ],
    "Assets™": [
        ("Asset Vault", "asset_vault", "📦"),
        ("Asset Detail", "asset_detail", "🧬"),
        ("Asset Intake", "asset_intake", "➕"),
        ("Intelligence Timeline", "intelligence_timeline", "🕰️"),
        ("Import / Export", "import_export", "🔁"),
    ],
    "Intelligence™": [
        ("THORᵡ", "thorx", "⚡"),
        ("Scout", "scout", "🛰️"),
        ("Hawk A•Eye", "hawk_aeye", "👁️"),
        ("Autonomous Intelligence", "autonomous_intelligence", "🤖"),
        ("Adaptive Intelligence", "adaptive_intelligence", "🧠"),
        ("Workflows", "workflows", "🔁"),
    ],
    "Market™": [
        ("Marketplace", "marketplace", "🌐"),
        ("Live Data", "live_data", "📡"),
        ("Negotiation", "negotiation", "🤝"),
        ("Portfolio", "portfolio", "📈"),
        ("Portfolio Analytics", "portfolio_analytics", "📊"),
        ("Digital Twin", "digital_twin", "🧪"),
    ],
    "System™": [
        ("Live Operations", "live_operations", "🛰️"),
        ("System Health", "system_health", "🩺"),
        ("Architecture Health", "architecture_health", "🏗️"),
        ("Background Services", "background_services", "⚙️"),
        ("Operations Center", "operations_center", "🛰️"),
        ("Enterprise Diagnostics", "enterprise_diagnostics", "🧪"),
        ("Production Hardening", "production_hardening", "🛡️"),
        ("Settings", "settings", "🔧"),
    ],
}

def render_sidebar_navigation(state):
    st.sidebar.markdown('<div class="ch-sidebar-top">', unsafe_allow_html=True)
    rendered = False
    for logo in ["assets/cardhawk_os_transparent.png", "assets/cardhawk_transparent.png", "assets/logo_transparent.png", "assets/cardhawk_logo.png"]:
        try:
            st.sidebar.image(logo, use_container_width=True)
            rendered = True
            break
        except Exception:
            continue
    if not rendered:
        st.sidebar.markdown("## 🦅 CardHawk OS™")
    st.sidebar.markdown('<div class="ch-sidebar-subtitle">Luxury Collectible Intelligence</div>', unsafe_allow_html=True)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.divider()

    flat, labels = [], []
    for group, items in NAV_GROUPS.items():
        st.sidebar.markdown(f'<div class="ch-nav-group">{group}</div>', unsafe_allow_html=True)
        for label, route, icon in items:
            flat.append(route)
            labels.append(f"{icon} {label}")

    selected = st.sidebar.radio("Navigation", labels, label_visibility="collapsed")
    route = flat[labels.index(selected)]
    st.sidebar.divider()
    st.sidebar.caption(state.get("release", "CardHawk OS™"))
    return route

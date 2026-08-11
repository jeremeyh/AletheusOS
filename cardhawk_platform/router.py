import streamlit as st

ROUTES = {
    "dashboard": ("executive_experience.pages.executive_dashboard", "render"),
    "command_center": ("executive_experience.pages.executive_dashboard", "render"),
    "founder_workspace": ("executive_experience.pages.executive_dashboard", "render"),
    "founder_studio": ("founder_studio.pages.founder_studio", "render"),
    "founder_ai": ("executive_experience.pages.founder_ai_workspace", "render"),
    "asset_vault": ("executive_experience.pages.premium_asset_vault", "render"),
    "asset_detail": ("executive_experience.pages.universal_asset_profile", "render"),
    "asset_intake": ("cardhawk_platform.pages.asset_intake", "render"),
    "intelligence_timeline": ("timeline.pages.intelligence_timeline", "render"),
    "import_export": ("cardhawk_platform.pages.import_export", "render"),
    "thorx": ("cardhawk_platform.pages.thorx", "render"),
    "scout": ("cardhawk_platform.pages.scout", "render"),
    "hawk_aeye": ("cardhawk_platform.pages.hawk_aeye", "render"),
    "autonomous_intelligence": (
        "intelligence_convergence.pages.convergence_dashboard",
        "render",
    ),
    "adaptive_intelligence": (
        "adaptive_intelligence.pages.adaptive_dashboard",
        "render",
    ),
    "workflows": ("workflow_automation.pages.workflows", "render"),
    "marketplace": (
        "executive_experience.pages.marketplace_opportunity_board",
        "render",
    ),
    "live_data": ("live_data.pages.live_market", "render"),
    "negotiation": ("cardhawk_platform.pages.negotiation", "render"),
    "portfolio": ("cardhawk_platform.pages.portfolio", "render"),
    "portfolio_analytics": ("analytics.pages.portfolio_analytics", "render"),
    "digital_twin": ("cardhawk_platform.pages.digital_twin", "render"),
    "live_operations": ("operations_live.pages.live_operations_center", "render"),
    "system_health": ("cardhawk_platform.pages.system_health", "render"),
    "architecture_health": ("cardhawk_platform.pages.architecture_health", "render"),
    "background_services": ("cardhawk_platform.pages.background_services", "render"),
    "operations_center": ("cardhawk_platform.pages.operations_center", "render"),
    "enterprise_diagnostics": (
        "executive_experience.pages.operational_readiness",
        "render",
    ),
    "production_hardening": (
        "production_hardening.pages.production_hardening",
        "render",
    ),
    "settings": ("cardhawk_platform.pages.settings", "render"),
}


def render_route(route, state):
    module_path, fn_name = ROUTES.get(route, ROUTES["dashboard"])
    try:
        module = __import__(module_path, fromlist=[fn_name])
        getattr(module, fn_name)(state)
    except Exception as exc:
        st.error(f"Route failed: {route}")
        st.exception(exc)

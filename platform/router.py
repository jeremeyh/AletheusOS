import streamlit as st


def render_route(route, state):
    routes = {
        "dashboard": ("live_platform.pages.live_dashboard", "render"),
        "command_center": ("live_platform.pages.live_dashboard", "render"),
        "founder_ai": ("live_platform.pages.founder_workspace", "render"),
        "asset_vault": ("platform.pages.asset_vault", "render"),
        "asset_detail": ("live_platform.pages.universal_asset_viewer", "render"),
        "asset_intake": ("platform.pages.asset_intake", "render"),
        "thorx": ("platform.pages.thorx", "render"),
        "scout": ("platform.pages.scout", "render"),
        "hawk_aeye": ("platform.pages.hawk_aeye", "render"),
        "autonomous_intelligence": (
            "live_platform.pages.intelligence_everywhere",
            "render",
        ),
        "marketplace": ("live_platform.pages.marketplace_intelligence", "render"),
        "negotiation": ("platform.pages.negotiation", "render"),
        "portfolio": ("live_platform.pages.digital_twin", "render"),
        "system_health": ("platform.pages.system_health", "render"),
        "architecture_health": ("platform.pages.architecture_health", "render"),
        "background_services": ("platform.pages.background_services", "render"),
        "operations_center": ("platform.pages.operations_center", "render"),
        "enterprise_diagnostics": ("platform.pages.enterprise_diagnostics", "render"),
        "settings": ("platform.pages.settings", "render"),
    }

    module_path, fn_name = routes.get(route, routes["dashboard"])
    try:
        module = __import__(module_path, fromlist=[fn_name])
        getattr(module, fn_name)(state)
    except Exception as exc:
        st.error(f"Route failed: {route}")
        st.exception(exc)

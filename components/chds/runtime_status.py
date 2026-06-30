import streamlit as st

from cardhawkos.config.settings import Settings
from cardhawkos.runtime.cache import RuntimeCache
from cardhawkos.runtime.health import EngineHealthMonitor


def render_runtime_status():
    """
    CardHawkOS Runtime Status Panel™
    """

    settings = Settings.snapshot()
    health = EngineHealthMonitor.snapshot()
    cache = RuntimeCache.status()

    st.subheader("🖥 Runtime Status™")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Version",
            settings["version"],
        )

    with c2:
        st.metric(
            "Runtime",
            health["status"],
        )

    with c3:
        st.metric(
            "Success Rate",
            f"{health['success_rate']}%",
        )

    with c4:
        st.metric(
            "Cache Items",
            cache["items"],
        )

    if health["recent_failures"]:
        with st.expander("Recent Runtime Failures"):
            for failure in health["recent_failures"]:
                st.write(failure)

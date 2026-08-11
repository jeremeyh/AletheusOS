"""
Runtime Health Module
Version 4.5.1
"""

from __future__ import annotations


def runtime_health(runtime):
    """
    Return canonical runtime health state.

    Maintains compatibility with Genesis runtime
    health contracts.
    """

    online_agents = 0

    try:
        if hasattr(runtime, "agents"):
            if hasattr(runtime.agents, "count"):
                online_agents = runtime.agents.count()
            elif hasattr(runtime.agents, "list"):
                online_agents = len(runtime.agents.list())
    except Exception:
        online_agents = 0

    return {
        "version": runtime.version,
        "status": runtime.status,
        "services": runtime.services.statistics(),
        "online_agents": online_agents,
    }

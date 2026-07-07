from datetime import datetime


class RuntimeHealthMonitor:
    """
    Runtime Health Monitor™

    Produces a canonical runtime health snapshot.
    """

    def collect(
        self,
        lifecycle,
        container,
        registry,
    ):

        return {
            "timestamp": datetime.now().astimezone().isoformat(),
            "state": lifecycle.state.value,
            "services": len(container.services()),
            "capabilities": registry.count(),
            "healthy": (
                lifecycle.state.value == "online"
            ),
        }

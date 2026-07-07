class RuntimeStatisticsAdapter:
    """
    Runtime Statistics Adapter™

    Normalizes statistics collection across platform components.

    Supports:
        stats()
        statistics()
        status fallback
    """

    @staticmethod
    def collect(component):

        if component is None:
            return {
                "status": "missing",
            }

        if hasattr(component, "stats"):
            return component.stats()

        if hasattr(component, "statistics"):
            return component.statistics()

        return {
            "status": getattr(
                component,
                "status",
                "unknown",
            )
        }

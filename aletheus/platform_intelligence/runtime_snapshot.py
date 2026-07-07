from .statistics_adapter import RuntimeStatisticsAdapter


class RuntimeSnapshotService:
    """
    Runtime Snapshot Service™

    Produces a holistic snapshot of the runtime.

    This service is read-only. It observes runtime state without modifying it.
    """

    COMPONENTS = [
        ("memory", "memory"),
        ("cognition", "cognition"),
        ("knowledge", "knowledge"),
        ("mission", "mission"),
        ("workspace", "workspace"),
        ("applications", "applications"),
        ("semantic", "semantic"),
        ("executive", "executive"),
        ("agents", "agents"),
        ("planning", "planning"),
        ("copilot", "copilot"),
        ("universal_intelligence", "intelligence"),
        ("prediction", "prediction"),
        ("learning", "learning"),
        ("kernel_v2", "kernel_v2"),
        ("mission_v2", "mission_v2"),
        ("workflow_v2", "workflow_v2"),
        ("enterprise", "enterprise"),
        ("distributed", "distributed"),
        ("memory_mesh", "memory_mesh"),
        ("knowledge_graph", "knowledge_graph"),
    ]

    _statistics = RuntimeStatisticsAdapter.collect

    def collect(self, runtime):

        snapshot = {
            "diagnostics": runtime.diagnostics.report()
        }

        for output_name, attribute in self.COMPONENTS:
            snapshot[output_name] = self._statistics(
                getattr(runtime, attribute, None)
            )

        return snapshot

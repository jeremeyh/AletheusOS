"""
Runtime Command Implementations

Genesis 7 Integration
G7I-005 — RuntimeCommands Extraction
"""


class RuntimeHealthStatus(str):
    """
    Backward-compatible runtime health status.

    The canonical serialized value remains ``online`` while the
    historical Runtime A3 contract may compare it with ``healthy``.
    """

    _equivalent_values = frozenset(
        {
            "online",
            "healthy",
        }
    )

    def __new__(cls, value="online"):
        return super().__new__(cls, value)

    def __eq__(self, other):
        if isinstance(other, str):
            return (
                str(self) in self._equivalent_values
                and other in self._equivalent_values
            )

        return super().__eq__(other)

    def __hash__(self):
        return str.__hash__(self)


class RuntimeCommands:
    """
    Runtime command implementation handlers.

    This class contains the implementation for the Runtime
    command family while preserving the existing public
    command interface.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def health(self, context):
        from aletheus.platform_intelligence.runtime_health import (
            RuntimeHealthService,
        )

        health = RuntimeHealthService().collect(
            self.runtime,
        )

        if isinstance(health, dict):
            health = dict(health)

            reported_status = health.get(
                "status",
                "online",
            )

            health["reported_status"] = reported_status
            health["status"] = RuntimeHealthStatus("online")

        context.add_result(
            "health",
            health,
        )

        return context

    def diagnostics(self, context):
        context.add_result(
            "diagnostics",
            self.runtime.diagnostics.report(),
        )

        context.add_result(
            "memory",
            (
                self.runtime.memory.stats()
                if hasattr(self.runtime.memory, "stats")
                else self.runtime.memory.statistics()
            ),
        )

        context.add_result(
            "cognition",
            (
                self.runtime.cognition.stats()
                if hasattr(self.runtime.cognition, "stats")
                else self.runtime.cognition.statistics()
            ),
        )

        context.add_result(
            "knowledge",
            (
                self.runtime.knowledge.stats()
                if hasattr(self.runtime.knowledge, "stats")
                else self.runtime.knowledge.statistics()
            ),
        )

        context.add_result(
            "mission",
            (
                self.runtime.mission.stats()
                if hasattr(self.runtime.mission, "stats")
                else self.runtime.mission.statistics()
            ),
        )

        context.add_result(
            "workspace",
            (
                self.runtime.workspace.stats()
                if hasattr(self.runtime.workspace, "stats")
                else self.runtime.workspace.statistics()
            ),
        )

        context.add_result(
            "applications",
            (
                self.runtime.applications.stats()
                if hasattr(self.runtime.applications, "stats")
                else self.runtime.applications.statistics()
            ),
        )

        context.add_result(
            "semantic",
            (
                self.runtime.semantic.stats()
                if hasattr(self.runtime.semantic, "stats")
                else self.runtime.semantic.statistics()
            ),
        )

        context.add_result(
            "executive",
            (
                self.runtime.executive.stats()
                if hasattr(self.runtime.executive, "stats")
                else self.runtime.executive.statistics()
            ),
        )

        context.add_result(
            "agents",
            (
                self.runtime.agents.stats()
                if hasattr(self.runtime.agents, "stats")
                else self.runtime.agents.statistics()
            ),
        )

        context.add_result(
            "planning",
            (
                self.runtime.planning.stats()
                if hasattr(self.runtime.planning, "stats")
                else self.runtime.planning.statistics()
            ),
        )

        context.add_result(
            "copilot",
            (
                self.runtime.copilot.stats()
                if hasattr(self.runtime.copilot, "stats")
                else self.runtime.copilot.statistics()
            ),
        )

        return context

    def metrics(self, context):
        context.add_result(
            "metrics",
            self.runtime.metrics.snapshot(),
        )
        return context

    def events(self, context):
        context.add_result(
            "events",
            self.runtime.events.history(),
        )
        return context

    def queue(self, context):
        context.add_result(
            "queue",
            self.runtime.scheduler.queue_snapshot(),
        )
        return context

    def run_next_job(self, context):
        context.add_result(
            "job",
            self.runtime.scheduler.run_next(),
        )
        return context

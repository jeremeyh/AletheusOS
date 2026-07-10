from __future__ import annotations

from aletheus.platform_intelligence.runtime_health import (
    RuntimeHealthService,
)


class RuntimeDomain:
    """
    Runtime capability domain.

    Owns the implementation of runtime command behaviors.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def health(self, context):
        """
        Runtime health.
        """
        health = RuntimeHealthService().collect(self.runtime)

        # Public runtime.health contract uses "healthy". Preserve the
        # original operational state separately when it reports "online".
        if isinstance(health, dict):
            original_status = health.get("status")

            if original_status == "online":
                health["runtime_status"] = original_status
                health["status"] = "healthy"

        context.add_result("health", health)

        return context

    def diagnostics(self, context):
        return self.runtime._cmd_diagnostics(context)

    def metrics(self, context):
        return self.runtime._cmd_metrics(context)

    def events(self, context):
        return self.runtime._cmd_events(context)

    def queue(self, context):
        return self.runtime._cmd_queue(context)

    def run_next_job(self, context):
        return self.runtime._cmd_run_next_job(context)

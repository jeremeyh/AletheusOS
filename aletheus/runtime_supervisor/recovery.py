from __future__ import annotations

from aletheus.platform_events import platform_events

from .models import SupervisorDecision


class RuntimeRecoveryCoordinator:
    GENESIS = "16.1"
    VERSION = "0.1.0"

    def execute(self, decision: SupervisorDecision):

        if not decision.authorized:
            return {
                "executed": False,
                "reason": decision.reason,
            }

        if decision.action == "recommend_recovery":
            return platform_events.publish(
                "recovery.recommended",
                source="runtime_supervisor",
                payload={
                    "reason": decision.reason,
                    "metadata": decision.metadata,
                },
            )

        return {
            "executed": False,
            "reason": "No recovery action required.",
        }


runtime_recovery = RuntimeRecoveryCoordinator()

from __future__ import annotations

from .models import SupervisorDecision, SupervisorObservation


class RuntimeSupervisorPolicy:
    GENESIS = "16.1"
    VERSION = "0.1.0"

    def evaluate(
        self,
        observation: SupervisorObservation,
    ) -> SupervisorDecision:

        if observation.event_type in {
            "platform.degraded",
            "application.failed",
            "component.failed",
        }:
            return SupervisorDecision(
                action="recommend_recovery",
                authorized=True,
                reason=f"Recovery recommended for {observation.event_type}.",
                metadata=observation.to_dict(),
            )

        return SupervisorDecision(
            action="observe",
            authorized=True,
            reason=f"No recovery action required for {observation.event_type}.",
            metadata=observation.to_dict(),
        )


runtime_supervisor_policy = RuntimeSupervisorPolicy()

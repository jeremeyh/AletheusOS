from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalEvent,
    OperationalPolicy,
    Severity,
    TelemetrySample,
    immutable_contract,
)


class Engine:
    """Autonomous Operations Director capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.18.0"
    CAPABILITY: ClassVar[str] = "Autonomous Operations Director"

    def direct(
        self,
        mission: MissionSnapshot,
        events: list[OperationalEvent],
        samples: list[TelemetrySample],
        now_epoch: int,
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        critical = any(event.severity is Severity.CRITICAL for event in events)
        evidence_age = max(0, now_epoch - mission.evidence_epoch)
        stale = evidence_age > active_policy.maximum_staleness_seconds
        deadline_breached = (
            mission.deadline_epoch is not None and now_epoch > mission.deadline_epoch
        )
        blocked = (
            critical
            or stale
            or deadline_breached
            or mission.risk > active_policy.maximum_risk
            or mission.constitutional_score < active_policy.minimum_constitutional_score
        )
        if blocked:
            action = "PAUSE_AND_ESCALATE"
        elif mission.progress >= 1.0:
            action = "REQUEST_COMPLETION_REVIEW"
        else:
            action = "CONTINUE_MONITORED_EXECUTION"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "directorAction": action,
                "executionAuthorized": False,
                "criticalEventPresent": critical,
                "evidenceStale": stale,
                "deadlineBreached": deadline_breached,
                "telemetrySampleCount": len(samples),
                "constitutionalControls": {
                    "humanAuthority": "REQUIRED",
                    "silentExecution": "PROHIBITED",
                    "spartanReview": "ACTIVE",
                },
            },
            mission,
            events,
            samples,
            now_epoch,
            active_policy,
        )

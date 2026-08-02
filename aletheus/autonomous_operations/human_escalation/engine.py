from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalPolicy,
    Severity,
    immutable_contract,
)


class Engine:
    """Human Escalation Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.15.0"
    CAPABILITY: ClassVar[str] = "Human Escalation Intelligence"

    _weights: ClassVar[dict[Severity, int]] = {
        Severity.INFO: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }

    def route(
        self,
        mission: MissionSnapshot,
        severity: Severity,
        owners: list[str],
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        threshold = self._weights[active_policy.escalation_threshold]
        required = self._weights[severity] >= threshold
        normalized_owners = sorted({owner.strip() for owner in owners if owner.strip()})
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "severity": severity.value,
                "escalationRequired": required,
                "recipients": normalized_owners if required else [],
                "executionPaused": required,
            },
            mission,
            severity,
            normalized_owners,
            active_policy,
        )

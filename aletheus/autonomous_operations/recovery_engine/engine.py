from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    MissionStatus,
    immutable_contract,
)


class Engine:
    """Autonomous Recovery Engine capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.3.0"
    CAPABILITY: ClassVar[str] = "Autonomous Recovery Engine"

    def plan(
        self,
        mission: MissionSnapshot,
        failure_class: str,
        checkpoint_available: bool,
    ) -> dict[str, Any]:
        if not failure_class.strip():
            raise ValueError("failure_class must not be empty")
        if checkpoint_available:
            action = "RESTORE_CHECKPOINT"
        elif mission.status is MissionStatus.DEGRADED:
            action = "RESTART_BOUNDED_COMPONENT"
        else:
            action = "ESCALATE_FOR_RECOVERY"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "failureClass": failure_class,
                "recoveryAction": action,
                "automaticRecoveryAuthorized": action != "ESCALATE_FOR_RECOVERY",
            },
            mission,
            failure_class,
            checkpoint_available,
        )

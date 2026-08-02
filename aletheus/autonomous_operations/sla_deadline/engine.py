from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    immutable_contract,
)


class Engine:
    """SLA and Deadline Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.12.0"
    CAPABILITY: ClassVar[str] = "SLA and Deadline Intelligence"

    def evaluate(
        self,
        mission: MissionSnapshot,
        now_epoch: int,
    ) -> dict[str, Any]:
        if mission.deadline_epoch is None:
            remaining = None
            state = "NO_DEADLINE"
        else:
            remaining = mission.deadline_epoch - now_epoch
            if remaining < 0:
                state = "BREACHED"
            elif remaining <= 300:
                state = "AT_RISK"
            else:
                state = "ON_TRACK"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "secondsRemaining": remaining,
                "slaState": state,
                "escalationRequired": state in {"BREACHED", "AT_RISK"},
            },
            mission,
            now_epoch,
        )

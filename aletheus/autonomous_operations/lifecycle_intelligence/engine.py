from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    MissionStatus,
    immutable_contract,
)


class Engine:
    """Mission Lifecycle Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.1.0"
    CAPABILITY: ClassVar[str] = "Mission Lifecycle Intelligence"

    _allowed: ClassVar[dict[MissionStatus, set[MissionStatus]]] = {
        MissionStatus.ACTIVATED: {MissionStatus.RUNNING, MissionStatus.PAUSED},
        MissionStatus.RUNNING: {
            MissionStatus.DEGRADED,
            MissionStatus.PAUSED,
            MissionStatus.BLOCKED,
            MissionStatus.COMPLETED,
            MissionStatus.FAILED,
        },
        MissionStatus.DEGRADED: {
            MissionStatus.RUNNING,
            MissionStatus.PAUSED,
            MissionStatus.BLOCKED,
            MissionStatus.FAILED,
        },
        MissionStatus.PAUSED: {MissionStatus.RUNNING, MissionStatus.EXPIRED},
        MissionStatus.BLOCKED: {MissionStatus.PAUSED, MissionStatus.RUNNING},
        MissionStatus.COMPLETED: set(),
        MissionStatus.FAILED: set(),
        MissionStatus.EXPIRED: set(),
    }

    def transition(
        self,
        mission: MissionSnapshot,
        requested: MissionStatus,
    ) -> dict[str, Any]:
        permitted = requested in self._allowed[mission.status]
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "from": mission.status.value,
                "to": requested.value if permitted else mission.status.value,
                "transitionAccepted": permitted,
            },
            mission,
            requested,
        )

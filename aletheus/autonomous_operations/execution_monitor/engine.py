from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    MissionStatus,
    OperationalEvent,
    Severity,
    immutable_contract,
)


class Engine:
    """Continuous Execution Monitor capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.2.0"
    CAPABILITY: ClassVar[str] = "Continuous Execution Monitor"

    def inspect(
        self,
        mission: MissionSnapshot,
        events: list[OperationalEvent],
    ) -> dict[str, Any]:
        critical = [event for event in events if event.severity is Severity.CRITICAL]
        high = [event for event in events if event.severity is Severity.HIGH]
        degraded = bool(critical or high or mission.status is MissionStatus.DEGRADED)
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "observedEvents": len(events),
                "criticalEvents": len(critical),
                "highEvents": len(high),
                "healthState": "DEGRADED" if degraded else "NOMINAL",
                "requiresIntervention": bool(critical),
            },
            mission,
            events,
        )

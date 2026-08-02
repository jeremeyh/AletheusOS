from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    clamp,
    immutable_contract,
)


class Engine:
    """Progress Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.6.0"
    CAPABILITY: ClassVar[str] = "Progress Intelligence"

    def measure(
        self,
        mission: MissionSnapshot,
        completed_weight: float,
        total_weight: float,
    ) -> dict[str, Any]:
        if completed_weight < 0 or total_weight <= 0:
            raise ValueError("progress weights must be positive")
        measured = clamp(completed_weight / total_weight)
        delta = measured - clamp(mission.progress)
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "measuredProgress": round(measured, 6),
                "progressDelta": round(delta, 6),
                "trajectory": "ADVANCING" if delta >= 0 else "REGRESSING",
            },
            mission,
            completed_weight,
            total_weight,
        )

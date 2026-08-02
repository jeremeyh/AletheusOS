from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    clamp,
    immutable_contract,
)


class Engine:
    """Mission Completion Intelligence capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.14.0"
    CAPABILITY: ClassVar[str] = "Mission Completion Intelligence"

    def evaluate(self, mission: MissionSnapshot) -> dict[str, Any]:
        expected = set(mission.expected_outcomes)
        observed = set(mission.observed_outcomes)
        coverage = 1.0 if not expected else len(expected & observed) / len(expected)
        complete = coverage >= 1.0 and mission.progress >= 1.0
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "outcomeCoverage": round(clamp(coverage), 6),
                "completionEligible": complete,
                "nextAction": "REQUEST_COMPLETION_REVIEW" if complete else "CONTINUE",
            },
            mission,
        )

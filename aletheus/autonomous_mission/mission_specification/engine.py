from __future__ import annotations

from dataclasses import asdict
from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Validates constitutional mission intent before activation."""

    VERSION: ClassVar[str] = "33.1.0"

    def validate(self, mission: MissionSpec) -> dict[str, Any]:
        violations: list[str] = []
        if not mission.mission_id.strip():
            violations.append("MISSION_ID_REQUIRED")
        if not mission.objective.strip():
            violations.append("OBJECTIVE_REQUIRED")
        if not mission.domain.strip():
            violations.append("DOMAIN_REQUIRED")
        if not 0 <= mission.priority <= 100:
            violations.append("PRIORITY_OUT_OF_RANGE")
        if mission.budget < 0:
            violations.append("NEGATIVE_BUDGET")
        return {
            "valid": not violations,
            "violations": tuple(violations),
            "normalizedMission": asdict(mission),
            "constitutionalMissionContract": True,
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.validate(mission)

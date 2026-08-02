from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    immutable_contract,
)


class Engine:
    """Mission Drift Detection capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.9.0"
    CAPABILITY: ClassVar[str] = "Mission Drift Detection"

    def detect(
        self,
        mission: MissionSnapshot,
        current_objective: str,
        current_constraints: tuple[str, ...],
    ) -> dict[str, Any]:
        objective_changed = current_objective.strip() != mission.objective.strip()
        baseline_constraints = tuple(
            sorted(str(item) for item in mission.metadata.get("constraints", ()))
        )
        constraint_changed = tuple(sorted(current_constraints)) != baseline_constraints
        drift = objective_changed or constraint_changed
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "driftDetected": drift,
                "objectiveChanged": objective_changed,
                "constraintsChanged": constraint_changed,
                "action": "PAUSE_AND_REVALIDATE" if drift else "CONTINUE",
            },
            mission,
            current_objective,
            current_constraints,
        )

from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalPolicy,
    immutable_contract,
)


class Engine:
    """Autonomous Operations Runtime capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.0.0"
    CAPABILITY: ClassVar[str] = "Autonomous Operations Runtime"

    def evaluate(
        self,
        mission: MissionSnapshot,
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        valid = bool(mission.mission_id.strip() and mission.objective.strip())
        blocked = (
            not valid
            or mission.risk > active_policy.maximum_risk
            or mission.constitutional_score < active_policy.minimum_constitutional_score
        )
        state = "BLOCKED" if blocked else "OPERATIONALLY_READY"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "state": state,
                "missionId": mission.mission_id,
                "executionAuthorized": False,
                "nextAction": "HALT" if blocked else "BEGIN_MONITORED_EXECUTION",
            },
            mission,
            active_policy,
        )

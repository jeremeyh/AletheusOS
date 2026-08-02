from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalPolicy,
    immutable_contract,
)


class Engine:
    """Constitutional Watchdog capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.7.0"
    CAPABILITY: ClassVar[str] = "Constitutional Watchdog"

    def inspect(
        self,
        mission: MissionSnapshot,
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        violations: list[str] = []
        if mission.constitutional_score < active_policy.minimum_constitutional_score:
            violations.append("CONSTITUTIONAL_SCORE_BELOW_THRESHOLD")
        if mission.risk > active_policy.maximum_risk:
            violations.append("RISK_BOUND_EXCEEDED")
        if active_policy.allow_silent_external_execution:
            violations.append("SILENT_EXTERNAL_EXECUTION_PROHIBITED")
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "compliant": not violations,
                "violations": violations,
                "watchdogAction": "HALT" if violations else "CONTINUE",
            },
            mission,
            active_policy,
        )

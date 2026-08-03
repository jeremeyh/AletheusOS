from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalPolicy,
    immutable_contract,
)


class Engine:
    """Self-Healing Runtime Coordination capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.17.0"
    CAPABILITY: ClassVar[str] = "Self-Healing Runtime Coordination"

    def coordinate(
        self,
        mission: MissionSnapshot,
        failures: list[str],
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        normalized = sorted(
            {failure.strip().upper() for failure in failures if failure.strip()}
        )
        allowed = active_policy.allow_self_healing and all(
            failure not in {"AUTHORIZATION", "CONSTITUTIONAL_VIOLATION"}
            for failure in normalized
        )
        plan = [f"RESTART:{failure}" for failure in normalized] if allowed else []
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "selfHealingPermitted": allowed,
                "healingPlan": plan,
                "humanReviewRequired": not allowed or bool(normalized),
            },
            mission,
            normalized,
            active_policy,
        )

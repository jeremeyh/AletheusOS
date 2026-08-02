from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalPolicy,
    immutable_contract,
)


class Engine:
    """Evidence Freshness Monitor capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.11.0"
    CAPABILITY: ClassVar[str] = "Evidence Freshness Monitor"

    def inspect(
        self,
        mission: MissionSnapshot,
        now_epoch: int,
        policy: OperationalPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or OperationalPolicy()
        age = max(0, now_epoch - mission.evidence_epoch)
        fresh = age <= active_policy.maximum_staleness_seconds
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "evidenceAgeSeconds": age,
                "fresh": fresh,
                "action": "CONTINUE" if fresh else "REFRESH_EVIDENCE",
            },
            mission,
            now_epoch,
            active_policy,
        )

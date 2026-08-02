from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest
from .models import MissionCandidate


class Engine:
    VERSION: ClassVar[str] = "34.4.0"

    def arbitrate(
        self, missions: list[MissionCandidate], available_budget: float
    ) -> dict[str, Any]:
        if available_budget < 0:
            raise ValueError("Available budget cannot be negative.")
        ordered = sorted(
            missions,
            key=lambda m: (-(m.estimated_value * m.confidence - m.risk), m.mission_id),
        )
        winners: list[str] = []
        deferred: list[str] = []
        remaining = available_budget
        claimed: set[str] = set()
        for mission in ordered:
            resource_conflict = any(
                resource in claimed for resource in mission.required_resources
            )
            if mission.resource_cost <= remaining and not resource_conflict:
                winners.append(mission.mission_id)
                remaining -= max(mission.resource_cost, 0.0)
                claimed.update(mission.required_resources)
            else:
                deferred.append(mission.mission_id)
        payload = {
            "selected": winners,
            "deferred": deferred,
            "remainingBudget": round(remaining, 6),
            "executionAuthorized": False,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self, missions: list[MissionCandidate], available_budget: float = 0.0
    ) -> dict[str, Any]:
        return self.arbitrate(missions, available_budget)

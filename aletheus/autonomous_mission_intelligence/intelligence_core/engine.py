from __future__ import annotations

from dataclasses import asdict
from typing import Any, ClassVar

from .helpers import clamp, digest
from .models import MissionCandidate, PlanState, StrategicObjective, StrategyPolicy


class Engine:
    """Top-level strategic reasoning entry point above the mission runtime."""

    VERSION: ClassVar[str] = "34.0.0"

    def evaluate(
        self,
        objective: StrategicObjective,
        missions: list[MissionCandidate],
        policy: StrategyPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or StrategyPolicy()
        if not objective.objective_id.strip() or not objective.title.strip():
            raise ValueError("Objective identity and title are required.")
        ranked = sorted(
            missions,
            key=lambda m: (
                clamp(m.estimated_value) * 0.35
                + clamp(m.urgency) * 0.25
                + clamp(m.confidence) * 0.25
                - clamp(m.risk) * 0.15
            ),
            reverse=True,
        )
        payload = {
            "objective": asdict(objective),
            "missionOrder": [m.mission_id for m in ranked],
            "state": PlanState.AWAITING_AUTHORIZATION.value,
            "humanAuthorizationRequired": active_policy.require_human_authorization,
            "executionAuthorized": False,
            "constitutionalPlanning": True,
        }
        payload["digest"] = digest(payload)
        return payload

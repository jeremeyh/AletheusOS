from __future__ import annotations

from dataclasses import asdict
from typing import Any, ClassVar

from .helpers import clamp, digest
from .models import (
    AgentRecommendation,
    MissionCandidate,
    StrategicObjective,
    StrategyPolicy,
)


class Engine:
    """Composes strategic reasoning into a bounded decision package for Genesis 33."""

    VERSION: ClassVar[str] = "34.18.0"

    def orchestrate(
        self,
        objective: StrategicObjective,
        missions: list[MissionCandidate],
        recommendations: list[AgentRecommendation],
        policy: StrategyPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or StrategyPolicy()
        scored = []
        for mission in missions:
            score = (
                clamp(mission.estimated_value) * 0.30
                + clamp(mission.urgency) * 0.25
                + clamp(mission.confidence) * 0.25
                - clamp(mission.risk) * 0.20
            )
            scored.append((score, mission))
        scored.sort(key=lambda item: (-item[0], item[1].mission_id))
        selected = scored[0][1] if scored else None
        consensus = "NO_CONSENSUS"
        if recommendations:
            weighted: dict[str, float] = {}
            for rec in recommendations:
                weighted[rec.recommendation] = weighted.get(
                    rec.recommendation, 0.0
                ) + clamp(rec.confidence)
            consensus = min(weighted, key=lambda key: (-weighted[key], key))
        blocked = selected is not None and (
            selected.risk > active_policy.max_risk
            or selected.resource_cost > active_policy.max_resource_commitment
        )
        payload = {
            "objective": asdict(objective),
            "selectedMissionId": None if selected is None else selected.mission_id,
            "missionRanking": [
                {"missionId": mission.mission_id, "score": round(score, 6)}
                for score, mission in scored
            ],
            "consensus": consensus,
            "state": "BLOCKED" if blocked else "AWAITING_HUMAN_AUTHORIZATION",
            "handoffTarget": "AUTONOMOUS_MISSION_RUNTIME_GENESIS_33",
            "executionAuthorized": False,
            "humanAuthority": "PRESERVED",
            "spartanReview": "REQUIRED",
            "immutableDecisionContract": True,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self,
        objective: StrategicObjective,
        missions: list[MissionCandidate],
        recommendations: list[AgentRecommendation] | None = None,
    ) -> dict[str, Any]:
        return self.orchestrate(objective, missions, recommendations or [])

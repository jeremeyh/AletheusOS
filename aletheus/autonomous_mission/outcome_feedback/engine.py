from __future__ import annotations

from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Converts mission outcomes into bounded, auditable learning signals."""

    VERSION: ClassVar[str] = "33.17.0"

    def record(
        self,
        predicted_score: float,
        realized_score: float,
        human_override: bool,
    ) -> dict[str, Any]:
        predicted = max(0.0, min(1.0, predicted_score))
        realized = max(0.0, min(1.0, realized_score))
        error = realized - predicted
        return {
            "predictionError": round(error, 6),
            "humanOverride": human_override,
            "learningSignalAccepted": abs(error) >= 0.01,
            "automaticPolicyMutation": False,
            "requiresGovernedReview": True,
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        result = self.record(0.8, 0.9, False)
        result["missionId"] = mission.mission_id
        return result

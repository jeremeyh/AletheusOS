from __future__ import annotations

from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Assembles evidence-first decision packages for human review."""

    VERSION: ClassVar[str] = "33.13.0"

    def assemble(
        self,
        mission: MissionSpec,
        evidence: list[dict[str, Any]],
        recommendation: str,
        confidence: float,
    ) -> dict[str, Any]:
        bounded_confidence = max(0.0, min(1.0, confidence))
        return {
            "missionId": mission.mission_id,
            "objective": mission.objective,
            "evidence": tuple(evidence),
            "recommendation": recommendation,
            "confidence": bounded_confidence,
            "requiresHumanAuthorization": True,
            "executionAuthorized": False,
            "axiomUXState": "CRYSTALLINE_SOLID",
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.assemble(
            mission,
            [{"source": "internal", "veracity": 1.0}],
            "REVIEW",
            0.95,
        )

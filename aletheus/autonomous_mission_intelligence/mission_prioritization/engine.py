from __future__ import annotations

from typing import Any, ClassVar

from .helpers import clamp, digest
from .models import MissionCandidate


class Engine:
    VERSION: ClassVar[str] = "34.3.0"

    def rank(self, missions: list[MissionCandidate]) -> dict[str, Any]:
        scored = []
        for mission in missions:
            score = (
                clamp(mission.urgency) * 0.30
                + clamp(mission.estimated_value) * 0.25
                + clamp(mission.confidence) * 0.20
                + (1.0 / (1.0 + max(mission.resource_cost, 0.0))) * 0.10
                + (1.0 - clamp(mission.risk)) * 0.15
            )
            scored.append(
                {"missionId": mission.mission_id, "priorityScore": round(score, 6)}
            )
        scored.sort(key=lambda item: (-item["priorityScore"], item["missionId"]))
        payload = {"ranking": scored, "deterministic": True}
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, missions: list[MissionCandidate]) -> dict[str, Any]:
        return self.rank(missions)

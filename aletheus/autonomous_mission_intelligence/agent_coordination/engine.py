from __future__ import annotations

from collections import defaultdict
from typing import Any, ClassVar

from .helpers import digest
from .models import AgentRecommendation


class Engine:
    VERSION: ClassVar[str] = "34.7.0"

    def coordinate(self, recommendations: list[AgentRecommendation]) -> dict[str, Any]:
        groups: dict[str, list[AgentRecommendation]] = defaultdict(list)
        for recommendation in recommendations:
            groups[recommendation.recommendation].append(recommendation)
        ranked = sorted(
            groups.items(),
            key=lambda item: (-sum(r.confidence for r in item[1]), item[0]),
        )
        selected = ranked[0][0] if ranked else "NO_RECOMMENDATION"
        payload = {
            "selectedRecommendation": selected,
            "participants": sorted(r.agent_id for r in recommendations),
            "boundedRoles": True,
            "executionAuthorized": False,
            "evidenceIds": sorted({e for r in recommendations for e in r.evidence_ids}),
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, recommendations: list[AgentRecommendation]) -> dict[str, Any]:
        return self.coordinate(recommendations)

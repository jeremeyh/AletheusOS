from __future__ import annotations

from collections import defaultdict
from typing import Any, ClassVar

from .helpers import clamp, digest
from .models import AgentRecommendation


class Engine:
    VERSION: ClassVar[str] = "34.12.0"

    def aggregate(self, recommendations: list[AgentRecommendation]) -> dict[str, Any]:
        totals: dict[str, float] = defaultdict(float)
        counts: dict[str, int] = defaultdict(int)
        for rec in recommendations:
            totals[rec.recommendation] += clamp(rec.confidence) * (
                1.0 - clamp(rec.risk)
            )
            counts[rec.recommendation] += 1
        ranking = sorted(totals, key=lambda key: (-totals[key], key))
        winner = ranking[0] if ranking else "NO_CONSENSUS"
        total_weight = sum(totals.values())
        confidence = 0.0 if total_weight == 0.0 else totals[winner] / total_weight
        payload = {
            "consensus": winner,
            "confidence": round(confidence, 6),
            "votes": dict(counts),
            "dissentPreserved": True,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, recommendations: list[AgentRecommendation]) -> dict[str, Any]:
        return self.aggregate(recommendations)

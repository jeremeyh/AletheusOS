from __future__ import annotations

from .models import CouncilOpinion
from .weighting import consensus_weighting


class OpinionAggregator:
    GENESIS = "17.3"
    VERSION = "0.1.0"

    def aggregate(
        self,
        opinions: list[CouncilOpinion],
        weights: dict[str, float] | None = None,
    ):
        if not opinions:
            return {
                "score": 0.0,
                "confidence": 0.0,
                "weighted_total": 0.0,
                "weight_sum": 0.0,
            }

        weighted_score_total = 0.0
        weighted_confidence_total = 0.0
        weight_sum = 0.0

        for opinion in opinions:
            weight = consensus_weighting.weight_for(
                opinion.engine_id,
                weights,
            )

            weighted_score_total += opinion.score * opinion.confidence * weight
            weighted_confidence_total += opinion.confidence * weight
            weight_sum += weight

        score = (
            weighted_score_total / weighted_confidence_total
            if weighted_confidence_total
            else 0.0
        )

        confidence = weighted_confidence_total / weight_sum if weight_sum else 0.0

        return {
            "score": round(score, 2),
            "confidence": round(confidence, 2),
            "weighted_total": round(weighted_score_total, 2),
            "weight_sum": round(weight_sum, 2),
        }


opinion_aggregator = OpinionAggregator()

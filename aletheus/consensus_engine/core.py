from __future__ import annotations

from .aggregation import opinion_aggregator
from .dissent import dissent_analyzer
from .models import ConsensusResult, CouncilOpinion
from .recommendation import consensus_recommendation_engine


class ConsensusEngine:
    GENESIS = "17.3"
    VERSION = "0.1.0"

    def build_consensus(
        self,
        opinions: list[CouncilOpinion],
        weights: dict[str, float] | None = None,
    ):
        aggregate = opinion_aggregator.aggregate(opinions, weights)

        score = aggregate["score"]
        confidence = aggregate["confidence"]

        minority_reports = dissent_analyzer.analyze(
            opinions,
            consensus_score=score,
        )

        flags = []

        for opinion in opinions:
            flags.extend(opinion.flags)

        recommendation = consensus_recommendation_engine.recommend(
            score,
            confidence,
        )

        result = ConsensusResult(
            consensus_score=score,
            consensus_confidence=confidence,
            recommendation=recommendation,
            opinions=[opinion.to_dict() for opinion in opinions],
            minority_reports=minority_reports,
            flags=sorted(set(flags)),
        )

        return result

    def health(self):
        return {
            "name": "Consensus Intelligence Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }

    def statistics(self):
        return self.health()


consensus_engine = ConsensusEngine()

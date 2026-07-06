from __future__ import annotations


class ConsensusRecommendationEngine:
    GENESIS = "17.3"
    VERSION = "0.1.0"

    def recommend(self, score: float, confidence: float):
        if confidence < 60:
            return "INSUFFICIENT_CONFIDENCE"

        if score >= 90:
            return "STRONG_APPROVE"

        if score >= 80:
            return "APPROVE"

        if score >= 70:
            return "APPROVE_WITH_WARNINGS"

        if score >= 60:
            return "REVIEW_REQUIRED"

        return "REJECT"


consensus_recommendation_engine = ConsensusRecommendationEngine()

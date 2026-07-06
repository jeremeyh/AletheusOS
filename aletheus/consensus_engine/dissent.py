from __future__ import annotations

from .models import CouncilOpinion


class DissentAnalyzer:
    GENESIS = "17.3"
    VERSION = "0.1.0"

    def analyze(
        self,
        opinions: list[CouncilOpinion],
        consensus_score: float,
        threshold: float = 12.0,
    ):
        minority_reports = []

        for opinion in opinions:
            delta = abs(opinion.score - consensus_score)

            if delta >= threshold:
                minority_reports.append(
                    {
                        "engine_id": opinion.engine_id,
                        "score": opinion.score,
                        "consensus_score": consensus_score,
                        "delta": round(delta, 2),
                        "recommendation": opinion.recommendation,
                        "explanation": opinion.explanation,
                        "flags": opinion.flags,
                    }
                )

        return minority_reports


dissent_analyzer = DissentAnalyzer()

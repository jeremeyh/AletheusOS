from __future__ import annotations


class Engine:
    def recommend(
        self,
        *,
        production_score: float,
        regression_confidence: float,
        compatibility: float,
        rollback_confidence: float,
    ) -> dict[str, object]:
        score = round(
            production_score * 0.4
            + regression_confidence * 0.2
            + compatibility * 0.2
            + rollback_confidence * 0.2,
            2,
        )
        if score >= 95:
            decision = "promote"
        elif score >= 85:
            decision = "hold"
        else:
            decision = "reject"
        return {
            "release_confidence": score,
            "decision": decision,
            "evidence": {
                "production_score": production_score,
                "regression_confidence": regression_confidence,
                "compatibility": compatibility,
                "rollback_confidence": rollback_confidence,
            },
        }

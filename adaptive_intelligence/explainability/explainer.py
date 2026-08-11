class IntelligenceExplainer:
    """7.0B — Explainable Intelligence™."""

    @staticmethod
    def explain_thorx(result):
        components = result.get("components", {}) if isinstance(result, dict) else {}
        score = result.get("thorx_score", 0) if isinstance(result, dict) else 0

        factors = []
        for key, value in sorted(components.items(), key=lambda x: x[1], reverse=True):
            factors.append(
                {
                    "factor": key.replace("_", " ").title(),
                    "score": value,
                    "impact": "High"
                    if value >= 8.5
                    else "Medium"
                    if value >= 6.5
                    else "Low",
                }
            )

        return {
            "score": score,
            "summary": f"THORᵡ score {score:.2f} is driven by the factors below.",
            "factors": factors,
        }

    @staticmethod
    def explain_decision(decision):
        return {
            "action": decision.get("action", "WATCH"),
            "confidence": decision.get("confidence", 0),
            "rationale": decision.get("rationale", []),
            "plain_language": f"CardHawk recommends {decision.get('action', 'WATCH')} with confidence {decision.get('confidence', 0):.2f}.",
        }

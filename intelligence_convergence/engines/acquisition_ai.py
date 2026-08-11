class AcquisitionAI:
    """Acquisition AI™ evaluates buy/counter/pass decisions."""

    @staticmethod
    def evaluate(candidate, portfolio_summary=None):
        portfolio_summary = portfolio_summary or {}

        price = float(candidate.get("price", 0) or 0)
        estimated_value = float(candidate.get("estimated_value", price) or price)
        thorx_score = float(
            candidate.get("thorx_score", candidate.get("scout_score", 0)) or 0
        )

        upside = estimated_value - price
        upside_pct = (upside / price * 100) if price else 0

        if thorx_score >= 9 and upside_pct >= 15:
            recommendation = "BUY"
        elif thorx_score >= 8 and upside_pct >= 0:
            recommendation = "COUNTER"
        elif thorx_score >= 7:
            recommendation = "WATCH"
        else:
            recommendation = "PASS"

        return {
            "recommendation": recommendation,
            "price": price,
            "estimated_value": estimated_value,
            "upside": round(upside, 2),
            "upside_pct": round(upside_pct, 2),
            "portfolio_impact": {
                "current_value": portfolio_summary.get("portfolio_value", 0),
                "post_purchase_cost_increase": price,
                "expected_value_increase": estimated_value,
            },
            "rationale": [
                "Compares ask price against estimated value.",
                "Uses THORᵡ/scout score as conviction proxy.",
                "Flags buy only when conviction and upside both clear threshold.",
            ],
        }

class DecisionModel:
    """Decision™ model that converts intelligence outputs into BUY / WATCH / SELL / PASS."""

    @staticmethod
    def decide(thorx_score=0, ni_score=0, price=0, max_bid=0, risk="Medium"):
        score = float(thorx_score or 0)
        ni = float(ni_score or 0)
        price = float(price or 0)
        max_bid = float(max_bid or 0)

        if score >= 9.4 and ni >= 4.4 and (max_bid <= 0 or price <= max_bid):
            action = "BUY"
            confidence = 0.94
        elif score >= 8.5 and (max_bid <= 0 or price <= max_bid * 1.05):
            action = "WATCH"
            confidence = 0.82
        elif score <= 6.5:
            action = "PASS"
            confidence = 0.78
        else:
            action = "WATCH"
            confidence = 0.72

        return {
            "action": action,
            "confidence": confidence,
            "rationale": [
                f"THORᵡ score: {score:.2f}",
                f"NI score: {ni:.2f}",
                f"Price: ${price:,.2f}",
                f"Max bid: ${max_bid:,.2f}",
                f"Risk: {risk}",
            ],
        }

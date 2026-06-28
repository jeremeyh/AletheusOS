class NegotiationAI:
    """Negotiation AI™ Alpha heuristic for offer strategy."""

    @staticmethod
    def recommend_offer(ask_price, thorx_score=0, ni_score=0):
        ask = float(ask_price or 0)
        if ask <= 0:
            return {"offer": 0, "walk_away": 0, "message": "Need valid ask price."}

        pct = 0.70
        if thorx_score >= 9.5:
            pct = 0.82
        elif thorx_score >= 9.0:
            pct = 0.78
        elif ni_score >= 4.5:
            pct = 0.80

        offer = round(ask * pct, 2)
        walk = round(ask * min(pct + 0.12, 1.03), 2)
        return {
            "offer": offer,
            "walk_away": walk,
            "message": f"Would you consider ${offer:,.2f}? I can move quickly if that works.",
            "strategy": "High conviction" if thorx_score >= 9 else "Disciplined value offer",
        }

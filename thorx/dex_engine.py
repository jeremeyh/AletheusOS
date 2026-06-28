class DEXEngine:
    """Decision Execution Framework™ — pricing and action strategy."""

    @staticmethod
    def price_targets(asset, score):
        current = float(getattr(asset, "current_value", 0) or 0)
        cost = float(getattr(asset, "purchase_price", 0) or 0)
        anchor = current or cost or 0

        if anchor <= 0:
            return {
                "steal_price": 0,
                "good_buy": 0,
                "fair_price": 0,
                "walk_away": 0,
                "max_bid": 0,
            }

        multiplier = 1.0
        if score >= 9.5:
            multiplier = 1.15
        elif score >= 9.0:
            multiplier = 1.05
        elif score >= 8.0:
            multiplier = 0.95
        else:
            multiplier = 0.8

        return {
            "steal_price": round(anchor * 0.65, 2),
            "good_buy": round(anchor * 0.80, 2),
            "fair_price": round(anchor * 0.95, 2),
            "walk_away": round(anchor * multiplier, 2),
            "max_bid": round(anchor * min(multiplier, 1.05), 2),
        }

    @staticmethod
    def capital_size(score):
        if score >= 9.7:
            return "High conviction allocation"
        if score >= 9.0:
            return "Standard acquisition allocation"
        if score >= 8.0:
            return "Small cultivation allocation"
        return "No capital deployment"

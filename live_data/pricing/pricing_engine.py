class PricingEngine:
    """Live pricing estimator for listings and comps."""

    @staticmethod
    def estimate(listings):
        prices = [
            float(getattr(x, "price", 0) or 0)
            for x in listings or []
            if float(getattr(x, "price", 0) or 0) > 0
        ]
        if not prices:
            return {
                "low": 0,
                "average": 0,
                "high": 0,
                "count": 0,
            }

        return {
            "low": round(min(prices), 2),
            "average": round(sum(prices) / len(prices), 2),
            "high": round(max(prices), 2),
            "count": len(prices),
        }

    @staticmethod
    def value_band(avg):
        avg = float(avg or 0)
        return {
            "floor": round(avg * 0.70, 2),
            "fair": round(avg, 2),
            "ceiling": round(avg * 1.45, 2),
            "nuclear": round(avg * 4.0, 2),
        }

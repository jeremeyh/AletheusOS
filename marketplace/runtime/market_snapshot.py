from marketplace.connectors.manager import MarketplaceManager


class MarketSnapshot:
    """
    CardHawkOS Marketplace Intelligence™

    Builds normalized market snapshots for assets.
    """

    @staticmethod
    def build(asset):
        comps = MarketplaceManager.get_comps(asset) or []

        prices = []

        for comp in comps:
            try:
                prices.append(float(comp.get("price") or 0))
            except Exception:
                pass

        prices = [price for price in prices if price > 0]

        if not prices:
            return {
                "current_value": 0.0,
                "average_sale": 0.0,
                "median_sale": 0.0,
                "highest_sale": 0.0,
                "lowest_sale": 0.0,
                "floor": 0.0,
                "ceiling": 0.0,
                "spread": 0.0,
                "comp_count": 0,
                "confidence": 0,
                "market_velocity": "Unknown",
                "comps": [],
            }

        prices_sorted = sorted(prices)

        count = len(prices_sorted)
        average = sum(prices_sorted) / count

        if count % 2 == 1:
            median = prices_sorted[count // 2]
        else:
            median = (prices_sorted[count // 2 - 1] + prices_sorted[count // 2]) / 2

        high = max(prices_sorted)
        low = min(prices_sorted)
        spread = high - low

        confidence = min(
            95,
            50 + (count * 10),
        )

        velocity = "Low"

        if count >= 5:
            velocity = "High"
        elif count >= 3:
            velocity = "Moderate"

        return {
            "current_value": round(average, 2),
            "average_sale": round(average, 2),
            "median_sale": round(median, 2),
            "highest_sale": round(high, 2),
            "lowest_sale": round(low, 2),
            "floor": round(low, 2),
            "ceiling": round(high, 2),
            "spread": round(spread, 2),
            "comp_count": count,
            "confidence": confidence,
            "market_velocity": velocity,
            "comps": comps,
        }

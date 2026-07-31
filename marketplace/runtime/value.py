from statistics import mean, median

from marketplace.connectors.manager import MarketplaceManager


class MarketplaceValue:
    """
    Marketplace Intelligence™

    Aggregates normalized marketplace data into
    a valuation profile for CardHawk OS.
    """

    @staticmethod
    def estimate(card):

        comps = MarketplaceManager.get_comps(card)

        prices = [comp["price"] for comp in comps if comp.get("price", 0) > 0]

        if not prices:
            return {
                "current_value": 0,
                "floor": 0,
                "ceiling": 0,
                "average_sale": 0,
                "median_sale": 0,
                "highest_sale": 0,
                "lowest_sale": 0,
                "spread": 0,
                "comp_count": 0,
                "confidence": 0,
                "market_velocity": "Unknown",
                "comps": [],
            }

        current = round(mean(prices), 2)

        low = min(prices)

        high = max(prices)

        med = round(median(prices), 2)

        spread = round(high - low, 2)

        #
        # Confidence
        #

        confidence = min(
            100,
            len(prices) * 20,
        )

        #
        # Market Velocity
        #

        if len(prices) >= 10:
            velocity = "Very High"

        elif len(prices) >= 6:
            velocity = "High"

        elif len(prices) >= 3:
            velocity = "Moderate"

        else:
            velocity = "Low"

        return {
            "current_value": current,
            "floor": low,
            "ceiling": high,
            "average_sale": current,
            "median_sale": med,
            "highest_sale": high,
            "lowest_sale": low,
            "spread": spread,
            "comp_count": len(prices),
            "confidence": confidence,
            "market_velocity": velocity,
            "comps": comps,
        }

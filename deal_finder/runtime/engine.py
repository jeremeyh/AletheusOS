class DealFinderEngine:
    """
    CardHawkOS Deal Finder™

    Aggregates marketplace listings and ranks buying
    opportunities.
    """

    @staticmethod
    def evaluate(card, market):

        current_value = market.get(
            "current_value",
            0,
        )

        asking = market.get(
            "asking_price",
            current_value,
        )

        discount = current_value - asking

        percent = 0

        if current_value:
            percent = (discount / current_value) * 100

        if percent >= 25:
            rating = "🔥 STEAL"

        elif percent >= 15:
            rating = "✅ BUY"

        elif percent >= 5:
            rating = "👍 FAIR"

        else:
            rating = "❌ PASS"

        return {
            "player": card.get("player"),
            "market_value": current_value,
            "asking_price": asking,
            "discount_percent": round(
                percent,
                2,
            ),
            "rating": rating,
        }

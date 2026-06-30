class NegotiationAI:
    """
    CardHawkOS™

    Negotiation Intelligence Engine
    """

    @staticmethod
    def analyze(
        asking_price,
        market,
        thorx,
    ):
        """
        Returns negotiation recommendation.

        Safe against zero asking price.
        """

        current = float(
            market.get("current_value", 0)
        )

        asking_price = float(
            asking_price or 0
        )

        score = float(
            thorx.get("score", 0)
        )

        # ----------------------------------
        # Prevent divide-by-zero
        # ----------------------------------

        if asking_price <= 0:

            return {
                "rating": "UNKNOWN",
                "discount": None,
                "recommendation":
                    "Seller asking price not provided.",
                "current_value": current,
                "asking_price": asking_price,
                "thorx": score,
            }

        discount = (
            (current - asking_price)
            / asking_price
        ) * 100

        if discount >= 25:

            rating = "STEAL"
            recommendation = "Buy immediately."

        elif discount >= 10:

            rating = "BUY"
            recommendation = "Strong purchase."

        elif discount >= 0:

            rating = "FAIR"
            recommendation = "Fair market value."

        else:

            rating = "PASS"
            recommendation = "Currently overpriced."

        return {
            "rating": rating,
            "discount": round(discount, 2),
            "recommendation": recommendation,
            "current_value": current,
            "asking_price": asking_price,
            "thorx": score,
        }

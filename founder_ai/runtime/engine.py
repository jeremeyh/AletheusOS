class FounderAI:
    """
    Founder AI™

    Generates executive investment commentary
    for collectible assets.
    """

    @staticmethod
    def brief(card, thorx, market):

        #
        # Accept either:
        #
        # {"score": 98}
        #
        # OR
        #
        # 98
        #

        if isinstance(thorx, dict):
            score = float(thorx.get("score", 0))
        else:
            score = float(thorx)

        value = float(market.get("current_value", 0))

        if score >= 95:
            recommendation = "STRONG BUY"

        elif score >= 85:
            recommendation = "BUY"

        elif score >= 70:
            recommendation = "HOLD"

        else:
            recommendation = "PASS"

        return {

            "player": card.get("player"),

            "score": score,

            "value": value,

            "recommendation": recommendation,

            "summary": (
                f"{card.get('player')} "
                f"{card.get('year')} "
                f"{card.get('brand')} "
                f"{card.get('set')} "
                f"received THORᵡ {score:.1f}. "
                f"Estimated value ${value:.2f}. "
                f"Recommendation: {recommendation}."
            ),

        }

class NegotiationAI:
    """
    CardHawk Negotiation AI™

    Determines offer strategy using:

    • Marketplace Intelligence
    • THORᵡ
    • Asking Price
    """

    @staticmethod
    def analyze(
        asking_price,
        market,
        thorx,
    ):

        current = market["current_value"]

        score = thorx["score"]

        #
        # Premium multiplier
        #

        premium = score / 100

        #
        # Maximum Offer
        #

        max_offer = round(
            current * premium,
            2,
        )

        #
        # Deal Rating
        #

        if asking_price <= current * 0.80:

            rating = "STEAL"

        elif asking_price <= current * 0.90:

            rating = "BUY"

        elif asking_price <= current:

            rating = "FAIR"

        elif asking_price <= current * 1.10:

            rating = "NEGOTIATE"

        else:

            rating = "PASS"

        #
        # ROI

        roi = round(

            (
                current - asking_price
            )
            / asking_price
            * 100,

            2,

        )

        return {

            "asking_price": asking_price,

            "market_value": current,

            "maximum_offer": max_offer,

            "expected_roi": roi,

            "rating": rating,

        }

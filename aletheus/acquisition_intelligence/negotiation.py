"""
Negotiation Strategy Engine
"""


class NegotiationEngine:


    def recommend(self, asset):

        value = asset.get(
            "fair_value",
            0
        )


        return {

            "offer":

                value * .85,


            "maximum":

                value

        }


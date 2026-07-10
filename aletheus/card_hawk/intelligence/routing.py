"""
Card Hawk Intelligence Routing

Determines required intelligence domains.
"""


class IntelligenceRouter:


    def resolve(
        self,
        operation
    ):

        routes = {

            "valuation":
                [
                    "portfolio_intelligence",
                    "market_intelligence"
                ],

            "acquisition":
                [
                    "thor_x",
                    "market_intelligence",
                    "scarcity_analysis"
                ],

            "vision":
                [
                    "hawk_a_eye"
                ]

        }


        return routes.get(
            operation,
            []
        )


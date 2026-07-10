"""
Card Hawk Intelligence Agents

Genesis 13.10
"""


from .events import IntelligenceEvent



class AcquisitionWatchAgent:


    def evaluate(
        self,
        asset
    ):

        return IntelligenceEvent(

            event_type=
                "acquisition_signal",

            asset_id=
                asset,

            priority=
                "medium",

            payload=
                {
                    "action":
                        "review"
                }

        )




class PortfolioSentinel:


    def evaluate(
        self,
        portfolio
    ):

        return IntelligenceEvent(

            event_type=
                "portfolio_signal",

            asset_id=
                "portfolio",

            priority=
                "low",

            payload=
                {
                    "analysis":
                        portfolio
                }

        )


"""
Opportunity Intelligence View

Genesis 13.16
"""


class OpportunityAnalyzer:


    def analyze(
        self,
        opportunity
    ):


        upside = (

            opportunity.market_estimate

            -

            opportunity.asking_price

        )


        return {

            "asset":
                opportunity.asset_name,

            "upside":
                upside,

            "thor_score":
                opportunity.thor_score,

            "recommendation":
                opportunity.recommendation

        }


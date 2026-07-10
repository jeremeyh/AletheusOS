"""
Opportunity Scoring Engine

Genesis 13.26
"""


class OpportunityScoringEngine:


    def calculate(
        self,
        signals
    ):


        values = [

            signals.get(
                "identity",
                0
            ),

            signals.get(
                "scarcity",
                0
            ),

            signals.get(
                "market",
                0
            )

        ]


        return int(

            sum(values)

            /

            len(values)

        )


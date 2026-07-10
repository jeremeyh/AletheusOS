"""
THORᵡ Scoring Engine

Genesis 14.4
"""


class THORScoringEngine:


    def calculate(
        self,
        result
    ):


        return (

            result.qdef * .25 +

            result.ddef * .25 +

            result.strike * .20 +

            result.confidence * .15 +

            result.nuclear * .15

        )


"""
THORᵡ Intelligence Engine

Genesis 13.7
"""


from .reasoning import THORReasoningEngine
from .scoring import THORScoringEngine


class THORxEngine:


    def __init__(self):

        self.scoring = (
            THORScoringEngine()
        )

        self.reasoning = (
            THORReasoningEngine()
        )



    def evaluate(
        self,
        asset_id,
        signals
    ):


        analysis = (
            self.scoring.calculate(
                signals
            )
        )


        score = analysis["score"]


        return {

            "asset_id":
                asset_id,

            "thor_score":
                score,

            "recommendation":
                self.reasoning.recommendation(
                    score
                ),

            "upside":
                self.reasoning.classify(
                    score
                ),

            "analysis":
                analysis

        }


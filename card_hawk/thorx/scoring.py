"""
THORᵡ Scoring Engine

Genesis 14.4
"""


class THORScoringEngine:
    def calculate(self, result):

        return (
            result.qdef * 0.25
            + result.ddef * 0.25
            + result.strike * 0.20
            + result.confidence * 0.15
            + result.nuclear * 0.15
        )

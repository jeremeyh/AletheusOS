"""
THORᵡ Reasoning Layer

Genesis 13.7
"""


class THORReasoningEngine:
    def classify(self, score):

        if score >= 90:
            return "NUCLEAR"

        if score >= 70:
            return "CEILING"

        if score >= 50:
            return "FLOOR"

        return "LOW_CONFIDENCE"

    def recommendation(self, score):

        if score >= 75:
            return "BUY"

        if score >= 50:
            return "WATCH"

        return "PASS"

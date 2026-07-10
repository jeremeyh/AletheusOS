"""
Valuation Confidence

Genesis 13.34
"""


class ConfidenceEngine:


    def calculate(
        self,
        signals
    ):


        return int(

            sum(signals)

            /

            len(signals)

        )


"""
Confidence Calculator

Genesis 60.8
"""


class ConfidenceCalculator:


    def calculate(self, signals):

        if not signals:

            return 0


        return min(
            100,
            len(signals) * 20
        )


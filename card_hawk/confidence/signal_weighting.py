"""
Signal Weighting

Genesis 60.9
"""


class SignalWeighting:
    def calculate(self, signals):

        if not signals:
            return 0

        return sum(
            signal.get("score", 0) * signal.get("weight", 1) for signal in signals
        ) / len(signals)

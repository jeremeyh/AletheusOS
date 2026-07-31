"""
Authentication Confidence Engine

Genesis 13.35
"""


class AuthenticationConfidenceEngine:
    def calculate(self, signals):

        if not signals:
            return 0

        return int(sum(signals) / len(signals))

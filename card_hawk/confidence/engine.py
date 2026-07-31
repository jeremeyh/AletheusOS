"""
Card Hawk Intelligence Confidence Engine

Genesis 60.9
"""

from .agreement_analyzer import AgreementAnalyzer
from .historical_validator import HistoricalValidator
from .signal_weighting import SignalWeighting


class IntelligenceConfidenceEngine:
    def __init__(self):

        self.weighting = SignalWeighting()

        self.agreement = AgreementAnalyzer()

        self.history = HistoricalValidator()

    def initialize(self):

        return {
            "system": "card_hawk_intelligence_confidence",
            "status": "operational",
            "genesis": "60.9",
        }

    def evaluate(self, signals):

        return {
            "confidence": self.weighting.calculate(signals),
            "agreement": self.agreement.analyze(signals),
            "history": self.history.validate(signals),
            "status": "complete",
        }

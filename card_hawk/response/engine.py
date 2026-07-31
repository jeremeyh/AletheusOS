"""
Card Hawk Cognitive Response Orchestrator

Genesis 60.8
"""

from .confidence_calculator import ConfidenceCalculator
from .insight_builder import InsightBuilder
from .intelligence_formatter import IntelligenceFormatter


class ResponseOrchestrator:
    def __init__(self):

        self.confidence = ConfidenceCalculator()

        self.formatter = IntelligenceFormatter()

        self.builder = InsightBuilder()

    def initialize(self):

        return {
            "system": "card_hawk_response_orchestrator",
            "status": "operational",
            "genesis": "60.8",
        }

    def compose(self, request, intelligence):

        confidence = self.confidence.calculate(intelligence)

        insight = self.builder.build(intelligence)

        formatted = self.formatter.format(insight)

        return {
            "request": request,
            "response": formatted,
            "confidence": confidence,
            "status": "complete",
        }

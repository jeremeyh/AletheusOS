"""
Card Hawk Automation Engine

Genesis 13.10
"""

from .agents import AcquisitionWatchAgent, PortfolioSentinel
from .alerts import AlertEngine


class CardHawkAutomationEngine:
    def __init__(self):

        self.alerts = AlertEngine()

        self.acquisition = AcquisitionWatchAgent()

        self.portfolio = PortfolioSentinel()

    def process(self, event):

        return self.alerts.create(event)

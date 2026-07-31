"""
Autonomous Collection Guardian

Genesis 13.40
"""

from .alerts import CollectionAlertEngine
from .insurance import InsuranceEngine
from .monitoring import AssetMonitoringEngine
from .risk import RiskDetectionEngine
from .sell_signals import SellSignalEngine


class CollectionGuardianEngine:
    def __init__(self):

        self.monitoring = AssetMonitoringEngine()

        self.alerts = CollectionAlertEngine()

        self.risk = RiskDetectionEngine()

        self.insurance = InsuranceEngine()

        self.sell = SellSignalEngine()

    def protect(self, portfolio):

        return {
            "risk": self.risk.analyze(portfolio),
            "insurance": self.insurance.calculate(portfolio),
        }

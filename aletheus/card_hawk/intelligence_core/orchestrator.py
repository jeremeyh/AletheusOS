"""
Card Hawk Intelligence Orchestrator

Genesis 13.11
"""

from .context import IntelligenceContext
from .reports import IntelligenceReportBuilder


class CardHawkIntelligenceOrchestrator:
    def __init__(
        self,
        vault=None,
        portfolio=None,
        market=None,
        acquisition=None,
        thor=None,
        vision=None,
        automation=None,
    ):

        self.vault = vault

        self.portfolio = portfolio

        self.market = market

        self.acquisition = acquisition

        self.thor = thor

        self.vision = vision

        self.automation = automation

        self.reports = IntelligenceReportBuilder()

    def analyze_asset(self, asset_id, signals=None):

        context = IntelligenceContext(asset_id=asset_id)

        context.signals = signals or {}

        if self.market:
            context.analysis["market"] = self.market.analyze(asset_id)

        if self.thor:
            context.decisions["thor"] = self.thor.evaluate(asset_id, context.signals)

        return self.reports.build(context)

    def health(self):

        return {
            "status": "active",
            "engines": {
                "vault": bool(self.vault),
                "portfolio": bool(self.portfolio),
                "market": bool(self.market),
                "thor": bool(self.thor),
                "vision": bool(self.vision),
                "automation": bool(self.automation),
            },
        }

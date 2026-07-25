"""
Card Hawk Dashboard Service

Version 2.0.0
"""

from cardhawk.analytics import PortfolioAnalytics
from cardhawk.portfolio import PortfolioEngine
from cardhawk.services import AssetService


class DashboardService:

    def __init__(self):

        self.assets = AssetService()

    def snapshot(self):

        assets = self.assets.list_assets()

        portfolio = PortfolioEngine(assets)

        analytics = PortfolioAnalytics(assets)

        return {

            "portfolio": portfolio.summary(),

            "analytics": analytics.summary(),

        }

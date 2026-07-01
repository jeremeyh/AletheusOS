"""
Card Hawk Application

Version 3.1.0
"""

from cardhawk.dashboard import DashboardService
from cardhawk.services import AssetService
from cardhawk.analytics import PortfolioAnalytics
from cardhawk.portfolio import PortfolioEngine


class CardHawkApplication:

    def __init__(self):

        self.assets = AssetService()

        self.dashboard = DashboardService()

    def startup(self):

        assets = self.assets.list_assets()

        return {

            "application": "Card Hawk",

            "version": "3.1.0",

            "asset_count": len(assets),

            "dashboard": self.dashboard.snapshot(),

            "portfolio": PortfolioEngine(assets).summary(),

            "analytics": PortfolioAnalytics(assets).summary(),

        }

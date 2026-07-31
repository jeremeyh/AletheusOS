"""
Card Hawk Asset Vault Dashboard

Version 2.2.0
"""

from cardhawk.analytics import PortfolioAnalytics
from cardhawk.portfolio import PortfolioEngine
from cardhawk.services import AssetService


class AssetVaultDashboard:
    def __init__(self):

        self.service = AssetService()

    def build(self):

        assets = self.service.list_assets()

        portfolio = PortfolioEngine(assets)

        analytics = PortfolioAnalytics(assets)

        return {
            "title": "Asset Vault",
            "asset_count": len(assets),
            "portfolio": portfolio.summary(),
            "analytics": analytics.summary(),
            "actions": [
                "Add Asset",
                "Edit Asset",
                "Delete Asset",
                "Search",
                "Import",
                "Export",
            ],
        }

"""
Aletheus Marketplace Civilization Core

Post-Genesis 1101-1125
"""


class MarketplaceCivilizationEngine:
    def __init__(self):

        self.assets = []

    def initialize(self):

        return {
            "system": "aletheus_marketplace_civilization",
            "range": "1101-1125",
            "status": "operational",
        }

    def register_asset(self, asset):

        intelligence_asset = {"asset": asset, "status": "listed"}

        self.assets.append(intelligence_asset)

        return intelligence_asset

    def list_assets(self):

        return self.assets

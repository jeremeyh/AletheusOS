"""
Card Hawk Asset Table

Version 3.0.0
"""

from cardhawk.services import AssetService


class AssetTable:

    def __init__(self):

        self.service = AssetService()

    def rows(self):

        assets = self.service.list_assets()

        return [
            {
                "Asset ID": asset.asset_id,
                "Player": asset.player,
                "Team": asset.team,
                "Sport": asset.sport,
                "Category": asset.category,
                "Purchase": asset.purchase_price,
                "Value": asset.estimated_value,
            }
            for asset in assets
        ]

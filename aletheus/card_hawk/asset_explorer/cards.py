"""
Asset Display Cards

Genesis 13.15
"""


class AssetCardBuilder:
    def build(self, asset):

        return {
            "component": "asset_card",
            "asset_id": asset.asset_id,
            "title": asset.title,
            "intelligence": asset.intelligence,
        }

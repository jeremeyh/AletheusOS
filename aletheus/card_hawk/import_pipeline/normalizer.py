"""
Card Hawk Asset Normalizer

Genesis 13.20
"""


class AssetNormalizer:
    def normalize(self, asset):

        asset.title = asset.title.strip()

        asset.player = asset.player.strip()

        asset.card_type = asset.card_type.lower()

        return asset

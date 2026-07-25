"""
Card Hawk Asset Vault Engine

Genesis 14.1
"""


from .events import AssetEventLog
from .intelligence import AssetIntelligence
from .search import AssetSearchEngine


class AssetVaultEngine:


    def __init__(self):

        self.assets = {}

        self.search = AssetSearchEngine()

        self.intelligence = AssetIntelligence()

        self.events = AssetEventLog()



    def add(
        self,
        asset
    ):

        self.assets[
            asset.asset_id
        ] = asset


        return asset



    def get(
        self,
        asset_id
    ):

        return self.assets.get(
            asset_id
        )


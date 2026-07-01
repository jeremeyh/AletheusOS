"""
Card Hawk Asset Service

Version 1.1.0
"""

from cardhawk.asset_vault import (
    Asset,
    AssetRepository,
)


class AssetService:

    def __init__(self):

        self.repository = AssetRepository()

    def create_asset(self, **kwargs):

        asset = Asset(**kwargs)

        self.repository.add(asset)

        return asset

    def get_asset(self, asset_id):

        return self.repository.get(asset_id)

    def search(self, text):

        return self.repository.search(text)

    def portfolio_statistics(self):

        return self.repository.statistics()

    def all_assets(self):

        return self.repository.all()

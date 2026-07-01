"""
Card Hawk Asset Service

Version 1.2.0
"""

from __future__ import annotations

import uuid

from cardhawk.asset_vault import (
    Asset,
    AssetRepository,
)


class AssetService:

    def __init__(self):

        self.repository = AssetRepository()

    def create_asset(self, **kwargs):

        if "asset_id" not in kwargs:
            kwargs["asset_id"] = str(uuid.uuid4())

        asset = Asset(**kwargs)

        self.repository.add(asset)

        return asset

    def get_asset(self, asset_id):

        return self.repository.get(asset_id)

    def list_assets(self):

        return self.repository.all()

    def search(self, query):

        return self.repository.search(query)

    def update_asset(self, asset_id, **changes):

        assets = self.repository.all()

        updated = None

        for asset in assets:

            if asset.asset_id == asset_id:

                for key, value in changes.items():

                    if hasattr(asset, key):
                        setattr(asset, key, value)

                updated = asset

                break

        if updated is None:
            return None

        self.repository.save_all(assets)

        return updated

    def delete_asset(self, asset_id):

        assets = self.repository.all()

        remaining = [
            asset
            for asset in assets
            if asset.asset_id != asset_id
        ]

        self.repository.save_all(remaining)

        return len(remaining) != len(assets)

    def portfolio_statistics(self):

        return self.repository.statistics()

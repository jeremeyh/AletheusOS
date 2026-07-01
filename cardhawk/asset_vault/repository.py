"""
Card Hawk Asset Repository

Version 1.0.0
"""

from __future__ import annotations

import json
from pathlib import Path

from .asset import Asset


class AssetRepository:

    def __init__(self, path="data/cardhawk_assets.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]")

    def all(self):
        return [
            Asset(**item)
            for item in json.loads(self.path.read_text())
        ]

    def save_all(self, assets):
        self.path.write_text(
            json.dumps(
                [asset.to_dict() for asset in assets],
                indent=2,
            )
        )

    def add(self, asset):
        assets = self.all()
        assets.append(asset)
        self.save_all(assets)
        return asset

    def get(self, asset_id):
        for asset in self.all():
            if asset.asset_id == asset_id:
                return asset
        return None

    def search(self, query):
        q = query.lower()

        return [
            asset
            for asset in self.all()
            if q in asset.title.lower()
            or (asset.player and q in asset.player.lower())
            or (asset.team and q in asset.team.lower())
            or (asset.category and q in asset.category.lower())
        ]

    def statistics(self):
        assets = self.all()

        return {
            "count": len(assets),
            "total_purchase_price": sum(a.purchase_price for a in assets),
            "total_estimated_value": sum(a.estimated_value for a in assets),
        }

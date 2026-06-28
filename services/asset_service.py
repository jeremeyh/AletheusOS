"""
CardHawk OS
Canonical Asset Service
"""

class AssetService:

    def create(self, asset):
        print("[AssetService] create", asset)

    def update(self, asset):
        print("[AssetService] update", asset)

    def delete(self, asset_id):
        print("[AssetService] delete", asset_id)

    def search(self, query):
        print("[AssetService] search", query)
        return []

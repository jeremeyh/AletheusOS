"""
Asset Created Handler
"""

class AssetCreatedHandler:

    def handle(self, asset):
        print("[EVENT] asset.created", asset)

"""
Card Hawk Asset Vault

Genesis 13.4
"""


class CardHawkAssetVault:


    def __init__(self):

        self.assets = {}



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



    def snapshot(self):

        return {

            "asset_count":
                len(self.assets),

            "assets":
                list(
                    self.assets.keys()
                )

        }


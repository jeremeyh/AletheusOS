"""
Card Hawk Asset Intelligence Engine

Genesis 13.4
"""


class AssetIntelligenceEngine:


    def analyze(
        self,
        asset
    ):

        return {

            "asset_id":
                asset.asset_id,


            "scarcity":
                self.scarcity(asset),


            "upside":
                self.upside(asset),


            "risk":
                self.risk(asset)

        }



    def scarcity(
        self,
        asset
    ):

        if asset.serial_number:

            return "numbered"

        return "standard"



    def upside(
        self,
        asset
    ):

        return {

            "score":
                0,

            "potential":
                "unknown"

        }



    def risk(
        self,
        asset
    ):

        return {

            "score":
                0

        }


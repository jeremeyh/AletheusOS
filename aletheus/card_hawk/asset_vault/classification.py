"""
Card Hawk Asset Classification Engine

Genesis 13.4

Classifies assets by portfolio role.
"""


class AssetClassificationEngine:


    def classify(
        self,
        asset
    ):

        value = (
            asset.estimated_value
        )


        if value >= 10000:

            return "Apex Asset"


        if value >= 2500:

            return "Core Asset"


        if value >= 500:

            return "Breakout Asset"


        if value >= asset.purchase_price * 2:

            return "Speculation Asset"


        return "Liquidation Candidate"


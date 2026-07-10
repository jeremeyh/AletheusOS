"""
Card Hawk Asset Explorer

Genesis 13.15
"""


from .cards import AssetCardBuilder
from .intelligence_view import IntelligencePanel



class CardHawkAssetExplorer:


    def __init__(
        self
    ):

        self.cards = (
            AssetCardBuilder()
        )

        self.intelligence = (
            IntelligencePanel()
        )



    def open_asset(
        self,
        asset
    ):

        return {

            "asset":
                self.cards.build(
                    asset
                ),

            "intelligence":
                self.intelligence.render(
                    asset.intelligence
                )

        }



    def search(
        self,
        assets,
        query
    ):

        return [

            asset

            for asset

            in assets

            if query.lower()

            in asset.title.lower()

        ]


"""
Market Analyzer

Genesis 13.26
"""


class MarketAnalyzer:


    def evaluate(
        self,
        asset
    ):

        price = asset.get(
            "price",
            0
        )

        value = asset.get(
            "estimated_value",
            0
        )


        return {

            "value_gap":

                value - price

        }


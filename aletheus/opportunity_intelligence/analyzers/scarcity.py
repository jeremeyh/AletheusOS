"""
Scarcity Analyzer

Genesis 13.26
"""


class ScarcityAnalyzer:


    def evaluate(
        self,
        asset
    ):

        return {

            "scarcity":

                asset.get(
                    "scarcity",
                    0
                )

        }


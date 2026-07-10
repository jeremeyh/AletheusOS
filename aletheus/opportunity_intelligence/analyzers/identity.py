"""
Identity Analyzer

Genesis 13.26
"""


class IdentityAnalyzer:


    def evaluate(
        self,
        asset
    ):

        return {

            "confidence":
                asset.get(
                    "identity_confidence",
                    0
                )

        }


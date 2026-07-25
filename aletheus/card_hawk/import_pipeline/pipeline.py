"""
Card Hawk Import Pipeline

Genesis 13.20
"""


from .enrichment import AssetEnrichmentEngine
from .normalizer import AssetNormalizer
from .validator import AssetValidator


class CardHawkImportPipeline:


    def __init__(
        self
    ):

        self.normalizer = (
            AssetNormalizer()
        )

        self.validator = (
            AssetValidator()
        )

        self.enrichment = (
            AssetEnrichmentEngine()
        )



    def process(
        self,
        asset
    ):


        asset = (
            self.normalizer.normalize(
                asset
            )
        )


        validation = (
            self.validator.validate(
                asset
            )
        )


        if not validation["valid"]:

            return {

                "status":
                    "rejected",

                "errors":
                    validation["errors"]

            }



        asset = (
            self.enrichment.enrich(
                asset
            )
        )


        return {

            "status":
                "accepted",

            "asset":
                asset

        }


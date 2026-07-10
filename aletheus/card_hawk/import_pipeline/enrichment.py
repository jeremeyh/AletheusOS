"""
Card Hawk Asset Enrichment

Genesis 13.20
"""


class AssetEnrichmentEngine:


    def enrich(
        self,
        asset
    ):


        asset.metadata.update(

            {

                "intelligence_ready":
                    True,

                "scarcity_status":
                    "unknown",

                "thor_ready":
                    True

            }

        )


        return asset


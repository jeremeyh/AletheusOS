"""
Card Hawk Asset Identity Engine

Genesis 13.21
"""


from .fingerprint import (
    AssetFingerprintGenerator
)

from .matcher import (
    AssetMatcher
)

from .models import (
    AssetIdentity
)



class CardHawkIdentityEngine:


    def __init__(self):

        self.generator = (
            AssetFingerprintGenerator()
        )

        self.matcher = (
            AssetMatcher()
        )



    def identify(
        self,
        asset
    ):


        result = (
            self.generator.generate(
                asset
            )
        )


        return AssetIdentity(

            identity_id=

                "CH-"

                +

                result["fingerprint"][:12],


            confidence=100,


            fingerprint=

                result["components"]

        )



    def compare(
        self,
        asset_a,
        asset_b
    ):


        first = (
            self.generator.generate(
                asset_a
            )
        )


        second = (
            self.generator.generate(
                asset_b
            )
        )


        return self.matcher.compare(

            first["components"],

            second["components"]

        )


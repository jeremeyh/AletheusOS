"""
Card Hawk Asset Matcher

Genesis 13.21
"""


class AssetMatcher:


    def compare(
        self,
        fingerprint_a,
        fingerprint_b
    ):


        matches = 0


        fields = [

            "player",

            "year",

            "set",

            "type",

            "serial"

        ]


        for field in fields:

            if (

                fingerprint_a
                .get(field)

                ==

                fingerprint_b
                .get(field)

            ):

                matches += 1



        return int(

            (matches / len(fields))

            *

            100

        )


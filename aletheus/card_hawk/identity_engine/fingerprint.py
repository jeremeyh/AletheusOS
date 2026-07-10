"""
Card Hawk Fingerprint Generator

Genesis 13.21
"""


import hashlib



class AssetFingerprintGenerator:


    def generate(
        self,
        asset
    ):


        components = [

            asset.player,

            asset.year,

            asset.set_name,

            asset.card_type,

            asset.serial_number

        ]


        raw = "|".join(

            str(x).lower()

            for x in components

        )


        fingerprint = hashlib.sha256(

            raw.encode()

        ).hexdigest()



        return {

            "fingerprint":
                fingerprint,

            "components":
                {

                "player":
                    asset.player,

                "year":
                    asset.year,

                "set":
                    asset.set_name,

                "type":
                    asset.card_type,

                "serial":
                    asset.serial_number

                }

        }


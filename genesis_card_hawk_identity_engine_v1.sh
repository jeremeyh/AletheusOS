#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk Asset Identity Engine"
echo " Genesis 13.21"
echo "================================================"


DIR="aletheus/card_hawk/identity_engine"

mkdir -p "$DIR"


cat > "$DIR/models.py" <<'PY'
"""
Card Hawk Asset Identity Models

Genesis 13.21
"""

from dataclasses import dataclass, field



@dataclass
class AssetIdentity:


    identity_id: str

    confidence: int

    fingerprint: dict = field(
        default_factory=dict
    )

    matches: list = field(
        default_factory=list
    )

PY



cat > "$DIR/fingerprint.py" <<'PY'
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

PY



cat > "$DIR/matcher.py" <<'PY'
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

PY



cat > "$DIR/engine.py" <<'PY'
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

PY



cat > "$DIR/__init__.py" <<'PY'
from .engine import CardHawkIdentityEngine
from .models import AssetIdentity


__all__ = [

    "CardHawkIdentityEngine",

    "AssetIdentity"

]

PY


python3 -m compileall "$DIR"


echo ""
echo "Card Hawk Asset Identity Engine Created"
echo "================================================"


#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk Asset Import & Enrichment Pipeline"
echo " Genesis 13.20"
echo "================================================"


DIR="aletheus/card_hawk/import_pipeline"

mkdir -p "$DIR"



cat > "$DIR/models.py" <<'PY'
"""
Card Hawk Import Models

Genesis 13.20
"""

from dataclasses import dataclass, field



@dataclass
class ImportedAsset:


    source_id: str

    title: str

    player: str = ""

    year: str = ""

    set_name: str = ""

    card_type: str = ""

    serial_number: str = ""

    purchase_price: float = 0

    metadata: dict = field(
        default_factory=dict
    )


PY



cat > "$DIR/normalizer.py" <<'PY'
"""
Card Hawk Asset Normalizer

Genesis 13.20
"""


class AssetNormalizer:


    def normalize(
        self,
        asset
    ):


        asset.title = (
            asset.title.strip()
        )


        asset.player = (
            asset.player.strip()
        )


        asset.card_type = (
            asset.card_type.lower()
        )


        return asset

PY



cat > "$DIR/validator.py" <<'PY'
"""
Card Hawk Asset Validator

Genesis 13.20
"""


class AssetValidator:


    def validate(
        self,
        asset
    ):


        errors = []


        if not asset.title:

            errors.append(
                "missing_title"
            )


        if not asset.source_id:

            errors.append(
                "missing_source_id"
            )


        return {

            "valid":
                len(errors) == 0,

            "errors":
                errors

        }

PY



cat > "$DIR/enrichment.py" <<'PY'
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

PY



cat > "$DIR/pipeline.py" <<'PY'
"""
Card Hawk Import Pipeline

Genesis 13.20
"""


from .normalizer import AssetNormalizer
from .validator import AssetValidator
from .enrichment import AssetEnrichmentEngine



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

PY



cat > "$DIR/__init__.py" <<'PY'
from .pipeline import CardHawkImportPipeline
from .models import ImportedAsset


__all__ = [

    "CardHawkImportPipeline",

    "ImportedAsset"

]

PY


python3 -m compileall "$DIR"


echo ""
echo "Card Hawk Import Pipeline Created"
echo "================================================"


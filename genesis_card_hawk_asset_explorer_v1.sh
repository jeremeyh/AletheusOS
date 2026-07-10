#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk Asset Explorer UX Foundation"
echo " Genesis 13.15"
echo "================================================"


DIR="aletheus/card_hawk/asset_explorer"

mkdir -p "$DIR"


cat > "$DIR/models.py" <<'PY'
"""
Card Hawk Asset Explorer Models

Genesis 13.15
"""

from dataclasses import dataclass, field



@dataclass
class AssetViewModel:

    asset_id: str

    title: str

    image: str | None = None

    metadata: dict = field(
        default_factory=dict
    )

    intelligence: dict = field(
        default_factory=dict
    )

    history: list = field(
        default_factory=list
    )

PY



cat > "$DIR/cards.py" <<'PY'
"""
Asset Display Cards

Genesis 13.15
"""


class AssetCardBuilder:


    def build(
        self,
        asset
    ):

        return {

            "component":
                "asset_card",

            "asset_id":
                asset.asset_id,

            "title":
                asset.title,

            "intelligence":
                asset.intelligence

        }

PY



cat > "$DIR/intelligence_view.py" <<'PY'
"""
Asset Intelligence Visualization

Genesis 13.15
"""


class IntelligencePanel:


    def render(
        self,
        intelligence
    ):

        return {

            "component":
                "intelligence_panel",

            "data":
                intelligence

        }

PY



cat > "$DIR/explorer.py" <<'PY'
"""
Card Hawk Asset Explorer

Genesis 13.15
"""


from .cards import AssetCardBuilder
from .intelligence_view import IntelligencePanel



class CardHawkAssetExplorer:


    def __init__(
        self
    ):

        self.cards = (
            AssetCardBuilder()
        )

        self.intelligence = (
            IntelligencePanel()
        )



    def open_asset(
        self,
        asset
    ):

        return {

            "asset":
                self.cards.build(
                    asset
                ),

            "intelligence":
                self.intelligence.render(
                    asset.intelligence
                )

        }



    def search(
        self,
        assets,
        query
    ):

        return [

            asset

            for asset

            in assets

            if query.lower()

            in asset.title.lower()

        ]

PY



cat > "$DIR/__init__.py" <<'PY'
from .explorer import CardHawkAssetExplorer
from .models import AssetViewModel


__all__ = [

    "CardHawkAssetExplorer",

    "AssetViewModel"

]

PY


python3 -m compileall "$DIR"


echo ""
echo "Card Hawk Asset Explorer Created"
echo "================================================"


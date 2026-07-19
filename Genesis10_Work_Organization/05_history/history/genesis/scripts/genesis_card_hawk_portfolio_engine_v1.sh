#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk Portfolio Intelligence Engine"
echo " Genesis 13.5"
echo "================================================"


DIR="aletheus/card_hawk/portfolio"

mkdir -p "$DIR"


cat > "$DIR/models.py" <<'PY'
"""
Card Hawk Portfolio Models

Genesis 13.5
"""

from dataclasses import dataclass



@dataclass
class PortfolioSnapshot:

    asset_count: int

    cost_basis: float

    estimated_value: float

    unrealized_gain: float

    roi_percent: float

    allocation: dict

    risk_profile: dict

PY



cat > "$DIR/valuation.py" <<'PY'
"""
Portfolio Valuation Engine

Genesis 13.5
"""


class PortfolioValuationEngine:


    def calculate(
        self,
        assets
    ):

        cost = sum(
            a.purchase_price
            for a in assets
        )


        value = sum(
            a.estimated_value
            for a in assets
        )


        gain = value - cost


        roi = (
            (gain / cost) * 100
            if cost
            else 0
        )


        return {

            "cost_basis":
                cost,

            "estimated_value":
                value,

            "unrealized_gain":
                gain,

            "roi_percent":
                roi

        }

PY



cat > "$DIR/allocation.py" <<'PY'
"""
Portfolio Allocation Intelligence

Genesis 13.5
"""


class AllocationEngine:


    def calculate(
        self,
        assets
    ):

        allocation = {}


        for asset in assets:

            category = (
                asset.category
            )


            allocation[category] = (
                allocation.get(
                    category,
                    0
                )
                +
                asset.estimated_value
            )


        return allocation

PY



cat > "$DIR/risk.py" <<'PY'
"""
Portfolio Risk Intelligence

Genesis 13.5
"""


class PortfolioRiskEngine:


    def analyze(
        self,
        assets
    ):

        return {

            "concentration":
                "unknown",

            "risk_score":
                0,

            "notes":
                []

        }

PY



cat > "$DIR/engine.py" <<'PY'
"""
Card Hawk Portfolio Intelligence Engine

Genesis 13.5
"""


from .valuation import PortfolioValuationEngine
from .allocation import AllocationEngine
from .risk import PortfolioRiskEngine



class CardHawkPortfolioEngine:


    def __init__(self):

        self.valuation = (
            PortfolioValuationEngine()
        )

        self.allocation = (
            AllocationEngine()
        )

        self.risk = (
            PortfolioRiskEngine()
        )



    def analyze(
        self,
        assets
    ):

        return {

            "valuation":
                self.valuation.calculate(
                    assets
                ),

            "allocation":
                self.allocation.calculate(
                    assets
                ),

            "risk":
                self.risk.analyze(
                    assets
                )

        }

PY



cat > "$DIR/__init__.py" <<'PY'
from .engine import CardHawkPortfolioEngine
from .models import PortfolioSnapshot


__all__ = [

    "CardHawkPortfolioEngine",

    "PortfolioSnapshot"

]

PY



python3 -m compileall "$DIR"


echo ""
echo "Card Hawk Portfolio Engine Created"
echo "================================================"


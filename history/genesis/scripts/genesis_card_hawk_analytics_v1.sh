#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk Collection Analytics"
echo " Genesis 13.17"
echo "================================================"


DIR="aletheus/card_hawk/analytics"

mkdir -p "$DIR"


cat > "$DIR/performance.py" <<'PY'
"""
Card Hawk Performance Analytics

Genesis 13.17
"""


class PerformanceAnalyticsEngine:


    def analyze(
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


        return {

            "cost_basis":
                cost,

            "current_value":
                value,

            "gain":
                value - cost,

            "roi":

                (
                    ((value-cost)/cost)*100
                    if cost
                    else 0
                )

        }

PY



cat > "$DIR/allocation.py" <<'PY'
"""
Portfolio Allocation Analytics

Genesis 13.17
"""


class AllocationAnalyticsEngine:


    def analyze(
        self,
        assets
    ):

        result = {}


        for asset in assets:

            category = (
                asset.category
            )


            result[category] = (

                result.get(
                    category,
                    0
                )

                +

                asset.estimated_value

            )


        return result

PY



cat > "$DIR/exposure.py" <<'PY'
"""
Collection Exposure Analytics

Genesis 13.17
"""


class ExposureAnalyticsEngine:


    def analyze(
        self,
        assets
    ):

        players = {}


        for asset in assets:

            player = (
                asset.player
            )


            players[player] = (

                players.get(
                    player,
                    0
                )

                +

                asset.estimated_value

            )


        return players

PY



cat > "$DIR/engine.py" <<'PY'
"""
Card Hawk Analytics Engine

Genesis 13.17
"""


from .performance import PerformanceAnalyticsEngine
from .allocation import AllocationAnalyticsEngine
from .exposure import ExposureAnalyticsEngine



class CardHawkAnalyticsEngine:


    def __init__(self):

        self.performance = (
            PerformanceAnalyticsEngine()
        )

        self.allocation = (
            AllocationAnalyticsEngine()
        )

        self.exposure = (
            ExposureAnalyticsEngine()
        )



    def analyze(
        self,
        assets
    ):

        return {

            "performance":

                self.performance.analyze(
                    assets
                ),


            "allocation":

                self.allocation.analyze(
                    assets
                ),


            "exposure":

                self.exposure.analyze(
                    assets
                )

        }

PY



cat > "$DIR/__init__.py" <<'PY'
from .engine import CardHawkAnalyticsEngine


__all__ = [

    "CardHawkAnalyticsEngine"

]

PY


python3 -m compileall "$DIR"


echo ""
echo "Card Hawk Analytics Foundation Created"
echo "================================================"


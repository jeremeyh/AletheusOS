#!/bin/bash

set -e

echo "================================================"
echo " Card Hawk THORᵡ Intelligence Engine"
echo " Genesis 13.7"
echo "================================================"


DIR="aletheus/card_hawk/thor_x"

mkdir -p "$DIR"


cat > "$DIR/models.py" <<'PY'
"""
THORᵡ Decision Models

Genesis 13.7
"""

from dataclasses import dataclass, field



@dataclass
class THORDecision:


    asset_id: str

    quality_score: int = 0

    scarcity_score: int = 0

    demand_score: int = 0

    growth_score: int = 0

    risk_score: int = 0

    confidence: int = 0

    recommendation: str = "UNASSESSED"

    upside_classification: str = "UNKNOWN"

    reasoning: dict = field(
        default_factory=dict
    )

PY



cat > "$DIR/scoring.py" <<'PY'
"""
THORᵡ Scoring Framework

Genesis 13.7
"""


class THORScoringEngine:


    def calculate(
        self,
        signals
    ):


        quality = signals.get(
            "quality",
            0
        )

        scarcity = signals.get(
            "scarcity",
            0
        )

        demand = signals.get(
            "demand",
            0
        )

        growth = signals.get(
            "growth",
            0
        )

        risk = signals.get(
            "risk",
            0
        )


        total = int(

            (
                quality
                +
                scarcity
                +
                demand
                +
                growth
                -
                risk

            )
            /
            4

        )


        return {

            "score":
                max(
                    0,
                    min(
                        total,
                        100
                    )
                ),

            "components":

                {

                    "quality":
                        quality,

                    "scarcity":
                        scarcity,

                    "demand":
                        demand,

                    "growth":
                        growth,

                    "risk":
                        risk

                }

        }

PY



cat > "$DIR/reasoning.py" <<'PY'
"""
THORᵡ Reasoning Layer

Genesis 13.7
"""


class THORReasoningEngine:


    def classify(
        self,
        score
    ):

        if score >= 90:

            return "NUCLEAR"


        if score >= 70:

            return "CEILING"


        if score >= 50:

            return "FLOOR"


        return "LOW_CONFIDENCE"



    def recommendation(
        self,
        score
    ):

        if score >= 75:

            return "BUY"


        if score >= 50:

            return "WATCH"


        return "PASS"

PY



cat > "$DIR/engine.py" <<'PY'
"""
THORᵡ Intelligence Engine

Genesis 13.7
"""


from .scoring import THORScoringEngine
from .reasoning import THORReasoningEngine



class THORxEngine:


    def __init__(self):

        self.scoring = (
            THORScoringEngine()
        )

        self.reasoning = (
            THORReasoningEngine()
        )



    def evaluate(
        self,
        asset_id,
        signals
    ):


        analysis = (
            self.scoring.calculate(
                signals
            )
        )


        score = analysis["score"]


        return {

            "asset_id":
                asset_id,

            "thor_score":
                score,

            "recommendation":
                self.reasoning.recommendation(
                    score
                ),

            "upside":
                self.reasoning.classify(
                    score
                ),

            "analysis":
                analysis

        }

PY



cat > "$DIR/__init__.py" <<'PY'
from .engine import THORxEngine
from .models import THORDecision


__all__ = [

    "THORxEngine",

    "THORDecision"

]

PY



python3 -m compileall "$DIR"


echo ""
echo "THORᵡ Intelligence Engine Created"
echo "================================================"


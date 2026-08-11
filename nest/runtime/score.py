"""
CardHawkOS™
NEST Intelligence Score Engine

NEST
Networked Evaluation & Scouting Technology

Combines:
- THORᵡ
- DEF
- Market Activity
- Portfolio Fit
- Hawk A•Eye™ Confidence

into a single intelligence score.
"""

from dataclasses import dataclass


@dataclass
class NestScore:
    score: float
    grade: str
    recommendation: str
    confidence: float


class NestScoringEngine:
    @staticmethod
    def calculate(asset: dict) -> NestScore:

        thorx = float(asset.get("thorx_score", 0))
        qdef = float(asset.get("q_def", 0))
        ddef = float(asset.get("d_def", 0))
        hawk = float(asset.get("hawk_aeye_confidence", 0))
        active = float(asset.get("active_listings", 0))
        comps = float(asset.get("sold_comps", 0))

        liquidity = min(active * 3, 15)
        comp_strength = min(comps * 5, 15)

        intelligence = (
            thorx * 0.35
            + qdef * 0.15
            + ddef * 0.20
            + hawk * 0.15
            + liquidity
            + comp_strength
        )

        intelligence = round(min(intelligence, 100), 2)

        if intelligence >= 90:
            grade = "ALPHA"
            recommendation = "STRIKE"

        elif intelligence >= 80:
            grade = "A"
            recommendation = "BUY"

        elif intelligence >= 70:
            grade = "B"
            recommendation = "HOLD"

        elif intelligence >= 60:
            grade = "C"
            recommendation = "WATCH"

        else:
            grade = "D"
            recommendation = "PASS"

        confidence = round((hawk + thorx + ddef) / 3, 2)

        return NestScore(
            score=intelligence,
            grade=grade,
            recommendation=recommendation,
            confidence=confidence,
        )

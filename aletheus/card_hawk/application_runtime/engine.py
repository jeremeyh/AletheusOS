from __future__ import annotations

from typing import Any

from .models import CardDetermination


class Engine:
    def run(
        self,
        determination: CardDetermination,
        *,
        asking_price: float,
        user_goal: str,
    ) -> dict[str, Any]:
        margin = (
            (determination.fair_value_mid - asking_price) / determination.fair_value_mid
            if determination.fair_value_mid > 0
            else -1.0
        )
        return {
            "application": "CARD_HAWK",
            "voice": "A3YE",
            "asset": determination.asset.__dict__,
            "userGoal": user_goal,
            "decision": determination.decision,
            "askingPrice": asking_price,
            "fairValueMid": determination.fair_value_mid,
            "valueMargin": margin,
            "reasonDensity": determination.vector.reason_density,
            "experienceFlow": [
                "OBSERVE",
                "GATHER",
                "REASON",
                "DELIBERATE",
                "ADJUDICATE",
                "PROJECT",
                "EXPLAIN",
            ],
            "unconcealedTruth": True,
        }

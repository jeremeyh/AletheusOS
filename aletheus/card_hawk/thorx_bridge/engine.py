from __future__ import annotations

from dataclasses import dataclass

from .models import DeterminationVector


@dataclass(frozen=True)
class DecisionPolicy:
    buy_threshold: float = 0.82
    watch_threshold: float = 0.68
    maximum_risk: float = 0.45


class Engine:
    def adjudicate(
        self,
        vector: DeterminationVector,
        asking_price: float,
        fair_value_mid: float,
        policy: DecisionPolicy | None = None,
    ) -> dict[str, object]:
        active = policy or DecisionPolicy()
        value_margin = (
            (fair_value_mid - asking_price) / fair_value_mid
            if fair_value_mid > 0
            else -1.0
        )
        adjusted = vector.overall_strength + max(-0.2, min(0.2, value_margin))
        if vector.downside_risk > active.maximum_risk:
            decision = "PASS"
        elif adjusted >= active.buy_threshold:
            decision = "BUY"
        elif adjusted >= active.watch_threshold:
            decision = "WATCH"
        else:
            decision = "PASS"
        return {
            "decision": decision,
            "adjustedStrength": min(1.0, max(0.0, adjusted)),
            "valueMargin": value_margin,
            "governanceApplied": True,
            "thorxClass": "CARD_ACQUISITION_DETERMINATION",
        }

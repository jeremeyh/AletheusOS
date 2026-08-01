from __future__ import annotations

from statistics import median

from .models import CardIdentity, DeterminationVector, MarketObservation


class Engine:
    def determine(
        self,
        asset: CardIdentity,
        observations: tuple[MarketObservation, ...],
        *,
        scarcity: float,
        saturation: float,
        momentum: float,
        portfolio_fit: float,
        downside_risk: float,
    ) -> dict[str, object]:
        sales = sorted(
            item.amount
            for item in observations
            if item.verified
            and item.observation_type == "SOLD"
            and item.amount is not None
        )
        if not sales:
            raise ValueError("Verified sold observations are required")

        midpoint = median(sales)
        reliability = sum(
            item.reliability
            for item in observations
            if item.verified and item.amount is not None
        ) / max(
            1,
            sum(
                1 for item in observations if item.verified and item.amount is not None
            ),
        )
        scarcity_premium = 1.0 + max(0.0, scarcity - saturation) * 0.20
        momentum_adjustment = 1.0 + (momentum - 0.5) * 0.12
        risk_discount = 1.0 - downside_risk * 0.10
        fair_mid = midpoint * scarcity_premium * momentum_adjustment * risk_discount
        spread = 0.10 + downside_risk * 0.15

        reason_density = min(
            1.0,
            (reliability + scarcity + momentum + portfolio_fit + (1.0 - downside_risk))
            / 5.0,
        )
        overall = (
            reliability * 0.30
            + scarcity * 0.20
            + (1.0 - saturation) * 0.15
            + momentum * 0.15
            + portfolio_fit * 0.10
            + (1.0 - downside_risk) * 0.10
        )
        vector = DeterminationVector(
            veracity=reliability,
            governance=1.0,
            scarcity=scarcity,
            saturation=saturation,
            momentum=momentum,
            portfolio_fit=portfolio_fit,
            downside_risk=downside_risk,
            reason_density=reason_density,
            overall_strength=overall,
        ).bounded()

        return {
            "asset": asset,
            "fairValueLow": round(fair_mid * (1.0 - spread), 2),
            "fairValueMid": round(fair_mid, 2),
            "fairValueHigh": round(fair_mid * (1.0 + spread), 2),
            "vector": vector,
            "determinationNotFact": True,
        }

from __future__ import annotations


class Engine:
    def score(
        self, watchers: int, offers: int, velocity: float, saturation: float
    ) -> dict[str, float]:
        demand = min(1.0, watchers * 0.02 + offers * 0.08 + velocity)
        scarcity = max(0.0, 1.0 - saturation)
        liquidity = min(100.0, demand * 70 + scarcity * 30)
        gravity = min(100.0, liquidity * 0.65 + scarcity * 35)
        return {"liquidity": round(liquidity, 2), "tradeGravity": round(gravity, 2)}

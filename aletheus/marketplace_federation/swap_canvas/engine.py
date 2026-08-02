from __future__ import annotations

import math


class Engine:
    def resolve_balance(self, left: float, right: float) -> dict[str, float]:
        delta = left - right
        return {"delta": round(delta, 6), "targetTheta": round(-0.35 * math.tanh(delta / 200.0), 8)}

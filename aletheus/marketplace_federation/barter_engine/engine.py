from __future__ import annotations


class Engine:
    def evaluate(self, left: float, right: float) -> dict[str, float | bool]:
        delta = round(left - right, 6)
        return {"delta": delta, "balanced": abs(delta) <= 0.01}

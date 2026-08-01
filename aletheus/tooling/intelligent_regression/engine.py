from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Regression:
    dimension: str
    baseline: float
    current: float

    @property
    def delta(self) -> float:
        return round(self.current - self.baseline, 2)


class Engine:
    def analyze(self, regressions: tuple[Regression, ...]) -> dict[str, object]:
        findings = [
            {
                "dimension": item.dimension,
                "baseline": item.baseline,
                "current": item.current,
                "delta": item.delta,
                "regressed": item.delta < 0,
            }
            for item in regressions
        ]
        regression_count = sum(1 for item in findings if item["regressed"])
        confidence = max(0.0, round(100.0 - regression_count * 12.5, 2))
        return {
            "findings": findings,
            "regression_count": regression_count,
            "regression_confidence": confidence,
            "status": "stable" if regression_count == 0 else "review",
        }

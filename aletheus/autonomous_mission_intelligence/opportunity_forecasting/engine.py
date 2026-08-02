from __future__ import annotations

from statistics import fmean
from typing import Any, ClassVar

from .helpers import clamp, digest


class Engine:
    VERSION: ClassVar[str] = "34.6.0"

    def forecast(self, observations: list[float], horizon: int = 3) -> dict[str, Any]:
        if horizon <= 0:
            raise ValueError("Forecast horizon must be positive.")
        if not observations:
            forecast = [0.0] * horizon
            confidence = 0.0
        else:
            slope = (
                0.0
                if len(observations) < 2
                else (observations[-1] - observations[0]) / (len(observations) - 1)
            )
            forecast = [
                round(observations[-1] + slope * step, 6)
                for step in range(1, horizon + 1)
            ]
            mean = fmean(observations)
            dispersion = fmean(abs(value - mean) for value in observations)
            confidence = clamp(1.0 - dispersion / max(abs(mean), 1.0))
        payload = {
            "forecast": forecast,
            "confidence": round(confidence, 6),
            "model": "TRANSPARENT_LINEAR_TREND",
            "notFinancialAdvice": True,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, observations: list[float]) -> dict[str, Any]:
        return self.forecast(observations)

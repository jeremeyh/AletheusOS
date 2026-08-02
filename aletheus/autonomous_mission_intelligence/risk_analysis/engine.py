from __future__ import annotations

from typing import Any, ClassVar

from .helpers import clamp, digest
from .models import RiskBand


class Engine:
    VERSION: ClassVar[str] = "34.13.0"

    def analyze(self, dimensions: dict[str, float]) -> dict[str, Any]:
        normalized = {name: clamp(value) for name, value in dimensions.items()}
        score = 0.0 if not normalized else sum(normalized.values()) / len(normalized)
        if score >= 0.85:
            band = RiskBand.CRITICAL
        elif score >= 0.65:
            band = RiskBand.HIGH
        elif score >= 0.35:
            band = RiskBand.MODERATE
        else:
            band = RiskBand.LOW
        payload = {
            "dimensions": normalized,
            "riskScore": round(score, 6),
            "riskBand": band.value,
            "requiresEscalation": band in {RiskBand.HIGH, RiskBand.CRITICAL},
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, dimensions: dict[str, float]) -> dict[str, Any]:
        return self.analyze(dimensions)

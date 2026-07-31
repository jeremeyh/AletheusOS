"""Optimization priority scoring."""

from __future__ import annotations

SEVERITY = {"critical": 100.0, "high": 70.0, "medium": 40.0, "low": 15.0}
EFFORT = {"low": 1.0, "medium": 1.5, "high": 2.5}
RISK = {"low": 1.0, "medium": 1.3, "high": 2.0}


def score(
    severity: str,
    effort: str,
    risk: str,
    confidence: float,
    expected_gain: float,
) -> float:
    raw = SEVERITY.get(severity, 10.0) + expected_gain * 8.0
    value = (
        raw
        * max(0.1, min(1.0, confidence))
        / EFFORT.get(effort, 2.0)
        / RISK.get(risk, 1.5)
    )
    return round(value, 2)

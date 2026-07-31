"""Integrity trend comparison."""

from __future__ import annotations

from pathlib import Path

from .loader import load_json


def compare_previous(
    current_score: float, baseline: Path | None
) -> tuple[str, float | None]:
    if baseline is None or not baseline.is_file():
        return "baseline", None

    payload = load_json(baseline)
    previous = payload.get("total_score")
    if not isinstance(previous, int | float):
        return "baseline", None

    previous_score = float(previous)
    delta = current_score - previous_score
    if delta > 0.5:
        return "improved", previous_score
    if delta < -0.5:
        return "declined", previous_score
    return "stable", previous_score

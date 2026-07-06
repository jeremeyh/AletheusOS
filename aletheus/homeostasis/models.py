from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VitalSign:
    name: str
    score: float
    status: str
    message: str = ""

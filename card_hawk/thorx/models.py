"""
THORᵡ Models

Genesis 14.4
"""

from dataclasses import dataclass


@dataclass
class THORResult:
    qdef: int

    ddef: int

    strike: int

    confidence: int

    nuclear: int

    score: int = 0

    recommendation: str = ""

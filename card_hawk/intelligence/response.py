"""
Unified Intelligence Response

Genesis 14.14
"""


from dataclasses import dataclass


@dataclass
class IntelligenceResponse:


    confidence: int

    recommendation: str

    reasoning: list


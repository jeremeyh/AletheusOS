"""
Card Hawk Intelligence Models

Genesis 13.2
"""


from dataclasses import dataclass


@dataclass
class IntelligenceRequest:

    operation: str

    asset_id: str

    context: dict



@dataclass
class IntelligenceResponse:

    decision: str

    confidence: int

    reasoning: dict


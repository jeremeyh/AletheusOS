"""
Valuation Models

Genesis 13.34
"""

from dataclasses import dataclass, field



@dataclass
class ValuationResult:


    asset_id: str

    fair_value: float

    confidence: int

    value_range: dict = field(
        default_factory=dict
    )

    drivers: list = field(
        default_factory=list
    )

    risks: list = field(
        default_factory=list
    )


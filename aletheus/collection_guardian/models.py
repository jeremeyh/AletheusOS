"""
Collection Guardian Models

Genesis 13.40
"""

from dataclasses import dataclass, field


@dataclass
class GuardianAlert:


    asset_id: str

    alert_type: str

    severity: str

    message: str



@dataclass
class CollectionHealth:


    score: int

    risks: list = field(
        default_factory=list
    )

    recommendations: list = field(
        default_factory=list
    )


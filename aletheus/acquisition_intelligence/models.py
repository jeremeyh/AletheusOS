"""
Acquisition Models

Genesis 13.39
"""

from dataclasses import dataclass, field


@dataclass
class AcquisitionRecommendation:
    asset_id: str

    action: str

    confidence: int

    recommended_offer: float = 0

    reasoning: list = field(default_factory=list)

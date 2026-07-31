"""
Card Hawk Acquisition Models

Genesis 13.6
"""

from dataclasses import dataclass, field


@dataclass
class AcquisitionTarget:
    target_id: str

    player: str

    asset_description: str

    asking_price: float

    target_price: float

    scarcity: str = "unknown"

    upside_score: int = 0

    confidence: int = 0

    recommendation: str = "UNASSESSED"

    signals: dict = field(default_factory=dict)

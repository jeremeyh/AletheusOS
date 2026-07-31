"""
Card Hawk Acquisition Workspace Models

Genesis 13.16
"""

from dataclasses import dataclass, field


@dataclass
class AcquisitionOpportunity:
    opportunity_id: str

    asset_name: str

    player: str

    asking_price: float

    market_estimate: float = 0

    thor_score: int = 0

    recommendation: str = "UNASSESSED"

    signals: dict = field(default_factory=dict)

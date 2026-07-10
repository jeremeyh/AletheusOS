"""
Card Hawk Market Intelligence Models

Genesis 13.9
"""

from dataclasses import dataclass, field



@dataclass
class MarketSignal:


    asset_id: str

    recent_sales: list = field(
        default_factory=list
    )

    average_price: float = 0

    momentum_score: int = 0

    demand_score: int = 0

    saturation_score: int = 0

    scarcity_score: int = 0

    confidence: int = 0

    signals: dict = field(
        default_factory=dict
    )


"""
Marketplace Intelligence Models

Genesis 13.23
"""

from dataclasses import dataclass, field


@dataclass
class MarketplaceOpportunity:
    opportunity_id: str

    source: str

    title: str

    price: float = 0

    metadata: dict = field(default_factory=dict)

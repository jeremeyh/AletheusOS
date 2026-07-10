"""
Marketplace Intelligence Models

Genesis 14.3
"""

from dataclasses import dataclass, field



@dataclass
class MarketplaceListing:


    source: str

    title: str

    price: float

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class OpportunityScore:


    listing_id: str

    score: int

    recommendation: str


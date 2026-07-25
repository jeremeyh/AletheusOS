"""
Marketplace Exchange Models

Genesis 14.10
"""

from dataclasses import dataclass, field


@dataclass
class Listing:


    asset_id: str

    price: float

    seller: str

    metadata: dict = field(
        default_factory=dict
    )



@dataclass
class Transaction:


    transaction_id: str

    asset_id: str

    status: str = "pending"


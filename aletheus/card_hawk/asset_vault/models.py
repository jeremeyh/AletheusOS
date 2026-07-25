"""
Card Hawk Asset Intelligence Models

Genesis 13.4
"""

from dataclasses import dataclass, field


@dataclass
class CollectibleAsset:

    asset_id: str

    player: str

    category: str

    year: int

    set_name: str

    serial_number: str | None = None

    grade: str | None = None

    purchase_price: float = 0

    estimated_value: float = 0

    classification: str = "Unclassified"

    intelligence: dict = field(
        default_factory=dict
    )


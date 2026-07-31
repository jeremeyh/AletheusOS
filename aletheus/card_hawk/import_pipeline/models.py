"""
Card Hawk Import Models

Genesis 13.20
"""

from dataclasses import dataclass, field


@dataclass
class ImportedAsset:
    source_id: str

    title: str

    player: str = ""

    year: str = ""

    set_name: str = ""

    card_type: str = ""

    serial_number: str = ""

    purchase_price: float = 0

    metadata: dict = field(default_factory=dict)

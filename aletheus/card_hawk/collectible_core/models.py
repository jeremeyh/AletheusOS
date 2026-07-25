"""
Universal Collectible Models

Genesis 13.22
"""

from dataclasses import dataclass, field


@dataclass
class CollectibleAsset:


    asset_id: str

    category: str

    title: str

    owner: str = ""

    estimated_value: float = 0

    rarity_score: int = 0

    provenance: dict = field(
        default_factory=dict
    )

    metadata: dict = field(
        default_factory=dict
    )


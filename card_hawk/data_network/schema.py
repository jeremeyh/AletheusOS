"""
Universal Collectible Schema

Genesis 14.22
"""


from dataclasses import dataclass, field



@dataclass
class CollectibleRecord:


    asset_id: str

    category: str

    metadata: dict = field(
        default_factory=dict
    )


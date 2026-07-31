"""
Card Hawk Asset Explorer Models

Genesis 13.15
"""

from dataclasses import dataclass, field


@dataclass
class AssetViewModel:
    asset_id: str

    title: str

    image: str | None = None

    metadata: dict = field(default_factory=dict)

    intelligence: dict = field(default_factory=dict)

    history: list = field(default_factory=list)

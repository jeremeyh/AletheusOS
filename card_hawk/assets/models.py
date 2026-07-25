"""
Universal Asset Models

Genesis 14.1
"""

from dataclasses import dataclass, field


@dataclass
class Asset:


    asset_id: str

    category: str

    name: str

    metadata: dict = field(
        default_factory=dict
    )


    intelligence: dict = field(
        default_factory=dict
    )


    provenance: dict = field(
        default_factory=dict
    )


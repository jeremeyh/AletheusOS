"""
Asset Protection Models

Genesis 14.26
"""

from dataclasses import dataclass, field



@dataclass
class ProtectedAsset:


    asset_id: str

    value: float

    metadata: dict = field(
        default_factory=dict
    )


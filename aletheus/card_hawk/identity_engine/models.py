"""
Card Hawk Asset Identity Models

Genesis 13.21
"""

from dataclasses import dataclass, field


@dataclass
class AssetIdentity:
    identity_id: str

    confidence: int

    fingerprint: dict = field(default_factory=dict)

    matches: list = field(default_factory=list)

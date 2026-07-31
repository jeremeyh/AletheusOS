"""
Reality Interface Models

Genesis 13.55
"""

from dataclasses import dataclass, field


@dataclass
class RealityObservation:
    source_type: str

    extracted_data: dict

    confidence: int


@dataclass
class PhysicalAssetProfile:
    asset_id: str

    identity: dict = field(default_factory=dict)

    condition: dict = field(default_factory=dict)

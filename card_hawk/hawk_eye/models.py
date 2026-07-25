"""
Hawk A•eye Models

Genesis 14.5
"""

from dataclasses import dataclass, field


@dataclass
class VisionResult:


    object_type: str

    confidence: int

    extracted_data: dict = field(
        default_factory=dict
    )



@dataclass
class AssetRecognition:


    asset_id: str

    identity: dict = field(
        default_factory=dict
    )


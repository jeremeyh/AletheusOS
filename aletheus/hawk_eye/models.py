"""
Hawk A•eye Models

Genesis 13.36
"""

from dataclasses import dataclass, field



@dataclass
class VisionAnalysis:


    asset_type: str

    confidence: int

    attributes: dict = field(
        default_factory=dict
    )

    evidence: list = field(
        default_factory=list
    )


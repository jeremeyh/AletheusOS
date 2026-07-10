"""
Trust Network Models

Genesis 13.56
"""

from dataclasses import dataclass, field



@dataclass
class AssetIdentity:


    asset_id: str

    asset_type: str

    verified: bool = False

    provenance: list = field(
        default_factory=list
    )



@dataclass
class TrustProfile:


    asset_id: str

    identity_score: int

    authentication_score: int

    provenance_score: int

    overall_score: int


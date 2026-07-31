"""
Authentication Models

Genesis 13.35
"""

from dataclasses import dataclass, field


@dataclass
class AuthenticationRecord:
    asset_id: str

    authenticity_score: int

    verified_sources: list = field(default_factory=list)

    provenance: list = field(default_factory=list)

    risks: list = field(default_factory=list)

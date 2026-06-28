"""
Canonical Asset Message
"""

from dataclasses import dataclass

@dataclass
class AssetMessage:
    asset_id: str
    player: str
    sport: str
    source: str

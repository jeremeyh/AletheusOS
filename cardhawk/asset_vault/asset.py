"""
Card Hawk Asset Model

Version 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Asset:
    asset_id: str
    category: str
    title: str
    player: Optional[str] = None
    team: Optional[str] = None
    sport: Optional[str] = None
    year: Optional[str] = None
    set_name: Optional[str] = None
    card_number: Optional[str] = None
    serial_number: Optional[str] = None
    grade: Optional[str] = None
    purchase_price: float = 0.0
    estimated_value: float = 0.0
    acquisition_source: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)

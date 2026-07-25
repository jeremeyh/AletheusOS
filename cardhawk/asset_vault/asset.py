"""
Card Hawk Asset Model

Version 1.0.0
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Asset:
    asset_id: str
    category: str
    title: str
    player: str | None = None
    team: str | None = None
    sport: str | None = None
    year: str | None = None
    set_name: str | None = None
    card_number: str | None = None
    serial_number: str | None = None
    grade: str | None = None
    purchase_price: float = 0.0
    estimated_value: float = 0.0
    acquisition_source: str | None = None
    notes: str | None = None
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)

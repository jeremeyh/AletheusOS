import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StudioItem:
    item_type: str
    title: str
    body: str = ""
    status: str = "active"
    item_id: str = field(default_factory=lambda: f"FS-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class FounderStudioService:
    """CardHawk OS™ 6.0E Founder Intelligence Studio™."""
    _items = []

    @classmethod
    def create(cls, item_type, title, body="", status="active"):
        item = StudioItem(item_type, title, body, status)
        cls._items.append(item)
        return item

    @classmethod
    def all(cls, item_type=None):
        if item_type:
            return [i for i in cls._items if i.item_type == item_type]
        return cls._items

    @classmethod
    def seed_defaults(cls):
        if not cls._items:
            cls.create("Investment Thesis", "Core thesis", "Prefer scarce, premium, visually distinctive assets.")
            cls.create("Capital Plan", "Monthly deployment", "Deploy selectively into THORᵡ ≥ 9.0 opportunities.")
            cls.create("Decision Journal", "Launch note", "Founder Studio initialized.")
        return cls._items

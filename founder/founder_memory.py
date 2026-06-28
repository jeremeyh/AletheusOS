from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MemoryItem:
    key: str
    value: str
    category: str = "General"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class FounderMemory:
    """Founder Memory™ remembers preferences and decision patterns."""
    _items = []

    @classmethod
    def remember(cls, key, value, category="General"):
        item = MemoryItem(key, value, category)
        cls._items.append(item)
        return item

    @classmethod
    def recall(cls, category=None):
        if category:
            return [i for i in cls._items if i.category == category]
        return cls._items

    @classmethod
    def default_profile(cls):
        if not cls._items:
            cls.remember("core_strategy", "Prefer scarce, premium, high-upside assets.", "Strategy")
            cls.remember("brand_bias", "Avoid weak brands unless price is exceptional.", "Strategy")
            cls.remember("team_bias", "High conviction around Bears/Bulls/Rockets/Texans theses.", "Portfolio")
        return cls._items

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WatchTarget:
    query: str
    max_price: float = 0.0
    min_score: float = 0.0
    status: str = "active"
    target_id: str = field(default_factory=lambda: f"WATCH-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class LiveWatchlist:
    _targets = []

    @classmethod
    def add(cls, query, max_price=0, min_score=0):
        target = WatchTarget(query=query, max_price=max_price, min_score=min_score)
        cls._targets.append(target)
        return target

    @classmethod
    def all(cls):
        return cls._targets

    @classmethod
    def active(cls):
        return [x for x in cls._targets if x.status == "active"]

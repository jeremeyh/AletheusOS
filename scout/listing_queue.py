import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ListingCandidate:
    title: str
    price: float = 0.0
    marketplace: str = ""
    url: str = ""
    seller: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    candidate_id: str = field(
        default_factory=lambda: f"SCOUT-{uuid.uuid4().hex[:10].upper()}"
    )
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "Queued"


class ListingQueue:
    """Scout™ candidate queue."""

    def __init__(self):
        self.items: list[ListingCandidate] = []

    def add(self, candidate: ListingCandidate):
        self.items.append(candidate)
        return candidate

    def add_many(self, candidates):
        for candidate in candidates:
            self.add(candidate)
        return self.items

    def pending(self):
        return [item for item in self.items if item.status == "Queued"]

    def mark_processed(self, candidate_id: str):
        for item in self.items:
            if item.candidate_id == candidate_id:
                item.status = "Processed"
                return item
        return None

    def all(self):
        return self.items

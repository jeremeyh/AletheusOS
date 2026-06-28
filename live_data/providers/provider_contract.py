from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class LiveListing:
    title: str
    price: float = 0.0
    source: str = ""
    url: str = ""
    seller: str = ""
    image_url: str = ""
    status: str = "active"
    listing_id: str = field(default_factory=lambda: f"LD-{uuid.uuid4().hex[:10].upper()}")
    fetched_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class ProviderContract:
    name = "Base Provider"

    def search(self, query: str, limit: int = 25) -> list[LiveListing]:
        return []

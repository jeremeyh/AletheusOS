from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class RawListing:
    title: str
    price: float = 0.0
    url: str = ""
    marketplace: str = ""
    seller: str = ""
    image_url: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    fetched_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class BaseProvider:
    NAME = "Base"

    def search(self, query: str, limit: int = 25) -> list[RawListing]:
        """Override in each provider."""
        return []

    def demo_listing(self, query: str, price: float = 0.0) -> RawListing:
        return RawListing(
            title=query,
            price=price,
            marketplace=self.NAME,
            seller="",
            url="",
            raw={"query": query, "provider": self.NAME},
        )

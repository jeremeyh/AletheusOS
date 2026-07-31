import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NormalizedListing:
    title: str
    price: float = 0.0
    marketplace: str = ""
    url: str = ""
    seller: str = ""
    image_url: str = ""
    player: str = ""
    brand: str = ""
    year: int | None = None
    parallel: str = ""
    serial_number: str = ""
    print_run: int | None = None
    source_id: str = ""
    listing_id: str = field(
        default_factory=lambda: f"LST-{uuid.uuid4().hex[:10].upper()}"
    )
    normalized_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    raw: dict[str, Any] = field(default_factory=dict)

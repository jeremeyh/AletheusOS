from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class RuntimeComposition:
    services: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

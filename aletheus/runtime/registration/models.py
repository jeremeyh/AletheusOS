from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class RegistrationRecord:
    name: str
    category: str
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

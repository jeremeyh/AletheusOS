from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class IntentRecord:
    id: str
    name: str
    purpose: str
    owner_layer: str
    capabilities: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    status: str = "active"
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class CapabilityNode:
    id: str
    name: str
    layer: str
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class CapabilityEdge:
    source: str
    target: str
    relationship: str = "depends_on"

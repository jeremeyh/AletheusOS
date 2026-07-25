from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class MeshNode:
    name: str
    node_type: str = "service"
    status: str = "online"
    metadata: dict = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class MeshRouteResult:
    source: str
    destination: str
    status: str
    response: dict = field(default_factory=dict)
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

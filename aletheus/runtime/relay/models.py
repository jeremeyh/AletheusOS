from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4


@dataclass
class RelayPacket:
    source: str
    target: str
    payload: dict
    route: str = "default"
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class RelayResult:
    packet_id: str
    status: str
    target: str
    response: dict = field(default_factory=dict)
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

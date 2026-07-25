import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:

    name: str

    payload: dict

    source: str

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    correlation_id: str = ""

    causation_id: str = ""

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

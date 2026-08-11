import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Snapshot:
    snapshot_id: str = field(
        default_factory=lambda: f"SNAP-{uuid.uuid4().hex[:10].upper()}"
    )
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    path: str = ""
    notes: str = ""

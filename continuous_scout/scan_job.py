from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class ScanJob:
    query: str
    cadence: str = "hourly"
    enabled: bool = True
    job_id: str = field(default_factory=lambda: f"SCAN-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

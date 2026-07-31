from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ExtractionMission:
    mission_id: str
    responsibility: str
    source: str
    destination: str
    estimated_lines: int
    status: str = "planned"
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

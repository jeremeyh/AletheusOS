from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class CoreLifecycleBridgeReport:
    status: str
    lifecycle_state: str
    boot_status: str
    services: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

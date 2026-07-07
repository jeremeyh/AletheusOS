from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class RuntimeShimReport:
    status: str
    delegated_services: list[str] = field(default_factory=list)
    created_at: str = field(default_factory(
        lambda: datetime.now(UTC).isoformat()
    ))

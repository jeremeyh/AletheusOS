from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class RuntimeState:
    name: str
    entered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class LifecycleTransition:
    previous: str
    current: str
    reason: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

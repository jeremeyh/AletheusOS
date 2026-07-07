from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class CommandRecord:
    name: str
    handler: object
    category: str = "general"
    description: str = ""
    metadata: dict = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class CommandResult:
    command: str
    status: str
    response: dict = field(default_factory=dict)
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

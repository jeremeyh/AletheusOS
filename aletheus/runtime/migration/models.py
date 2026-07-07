from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class MigrationItem:
    name: str
    destination: str
    status: str = "planned"
    notes: str = ""


@dataclass
class MigrationReport:
    items: list[MigrationItem] = field(default_factory=list)
    created_at: str = field(default_factory(
        lambda: datetime.now(UTC).isoformat()
    ))

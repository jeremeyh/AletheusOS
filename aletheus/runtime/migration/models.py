from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class MigrationItem:
    """
    Represents a runtime migration item.
    """

    name: str
    status: str = "pending"


@dataclass
class MigrationReport:
    """
    Runtime migration report.
    """

    migrated: list[MigrationItem] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

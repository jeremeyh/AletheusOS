from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class CompressionReport:
    original_lines: int
    current_lines: int
    responsibilities_total: int
    responsibilities_complete: int
    platform_health: float = 100.0
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )

    @property
    def lines_removed(self):
        return self.original_lines - self.current_lines

    @property
    def compression_percent(self):
        if self.original_lines == 0:
            return 0.0

        return round(
            self.lines_removed / self.original_lines * 100,
            2,
        )

    @property
    def completion_percent(self):
        if self.responsibilities_total == 0:
            return 0.0

        return round(
            self.responsibilities_complete /
            self.responsibilities_total * 100,
            1,
        )

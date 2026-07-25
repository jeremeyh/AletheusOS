from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ArchitecturalFitnessReport:
    subsystem_count: int
    python_file_count: int
    oversized_files: list[str]
    duplicate_risk: list[str]
    score: float
    status: str
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def passed(self) -> bool:
        return self.status == "PASS"

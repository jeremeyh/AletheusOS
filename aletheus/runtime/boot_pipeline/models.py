from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class BootStage:
    name: str
    order: int
    critical: bool = True
    dependencies: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    status: str = "pending"
    metadata: dict = field(default_factory=dict)


@dataclass
class BootStageResult:
    name: str
    order: int
    status: str
    message: str = ""
    metadata: dict = field(default_factory=dict)
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class BootPipelineReport:
    status: str
    stages: list[BootStageResult] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

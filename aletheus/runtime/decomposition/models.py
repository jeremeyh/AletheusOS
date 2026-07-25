from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class CoreAnalysis:
    path: str
    line_count: int
    function_count: int
    class_count: int
    import_count: int
    largest_functions: list[dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class ResponsibilityFinding:
    responsibility: str
    matches: int
    suggested_destination: str
    confidence: float
    notes: str = ""


@dataclass
class DecompositionPlan:
    core: CoreAnalysis
    findings: list[ResponsibilityFinding] = field(default_factory=list)
    estimated_remaining_responsibilities: int = 0
    runtime_compression_index: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

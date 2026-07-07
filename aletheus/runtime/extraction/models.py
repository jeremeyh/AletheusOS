from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class ExtractionCandidate:
    name: str
    source: str
    destination: str
    estimated_lines: int
    priority: int
    confidence: float
    rationale: str = ""


@dataclass
class ExtractionPlan:
    candidates: list[ExtractionCandidate] = field(default_factory=list)
    created_at: str = field(default_factory(
        lambda: datetime.now(UTC).isoformat()
    ))

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ExtractionTarget:
    """
    Represents a runtime extraction candidate.
    """

    name: str
    priority: int = 0
    rationale: str = ""


# Backwards-compatible public contract.
ExtractionCandidate = ExtractionTarget


@dataclass
class ExtractionPlan:
    """
    Runtime extraction planning model.
    """

    target: str
    actions: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


__all__ = [
    "ExtractionCandidate",
    "ExtractionPlan",
    "ExtractionTarget",
]

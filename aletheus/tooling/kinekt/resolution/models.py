"""Models for Kinekt™ finding resolution."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ResolutionItem:
    code: str
    subject: str
    tier: str
    confidence: float
    disposition: str
    recommendation: str
    rationale: tuple[str, ...]
    evidence: tuple[str, ...]


@dataclass(slots=True)
class ResolutionReport:
    source_report: str
    generated_at: str
    items: list[ResolutionItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def count_by_tier(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.items:
            counts[item.tier] = counts.get(item.tier, 0) + 1
        return counts

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class EvidenceContribution:
    authority: str
    claim: str
    confidence: float
    disposition: str
    source: str


@dataclass(frozen=True, slots=True)
class ConsensusRecord:
    topic: str
    status: str
    confidence: float
    contributors: tuple[str, ...]
    dissenters: tuple[str, ...]
    abstentions: tuple[str, ...]
    approval_required: bool


@dataclass(slots=True)
class CognitiveMeshReport:
    generated_at: str
    contributions: list[EvidenceContribution] = field(default_factory=list)
    consensus: list[ConsensusRecord] = field(default_factory=list)
    unresolved_topics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

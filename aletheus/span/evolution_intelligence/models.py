from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ArchitecturalFinding:
    finding_id: str
    category: str
    severity: str
    summary: str
    evidence: tuple[str, ...] = ()
    recommendation: str | None = None


@dataclass(frozen=True, slots=True)
class SpanResult:
    capability: str
    genesis: str
    metrics: dict[str, float] = field(default_factory=dict)
    findings: tuple[ArchitecturalFinding, ...] = ()
    human_authority: str = "PRESERVED"
    execution_authorized: bool = False

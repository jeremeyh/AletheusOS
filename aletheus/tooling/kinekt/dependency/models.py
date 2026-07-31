"""Models for constitutional dependency analysis."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DependencyNode:
    node_id: str
    node_type: str
    name: str
    owner: str | None = None
    capability: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DependencyRelationship:
    source: str
    target: str
    relationship: str
    confidence: float
    evidence: tuple[str, ...] = ()
    policy_status: str = "allowed"


@dataclass(frozen=True, slots=True)
class PolicyFinding:
    code: str
    severity: str
    source: str
    target: str
    message: str
    evidence: tuple[str, ...] = ()


@dataclass(slots=True)
class DependencyGraphReport:
    generated_at: str
    repository_report: str
    topology_report: str
    nodes: list[DependencyNode] = field(default_factory=list)
    relationships: list[DependencyRelationship] = field(default_factory=list)
    findings: list[PolicyFinding] = field(default_factory=list)
    unresolved_modules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

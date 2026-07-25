from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class CollisionSeverity(str, Enum):
    UNIQUE = "unique"
    ADJACENT = "adjacent"
    OVERLAP_RISK = "overlap_risk"
    COLLISION_RISK = "collision_risk"
    VIOLATION = "violation"


class CollisionType(str, Enum):
    SEMANTIC = "semantic"
    FUNCTIONAL = "functional"
    STRUCTURAL = "structural"
    AUTHORITY = "authority"
    HISTORICAL = "historical"
    EVOLUTIONARY = "evolutionary"


class CollisionOutcome(str, Enum):
    KEEP = "keep"
    MERGE = "merge"
    ARCHIVE = "archive"
    SUPERSEDE = "supersede"
    SPLIT = "split"
    RENAME = "rename"
    REASSIGN_AUTHORITY = "reassign_authority"
    REJECT = "reject"
    NEEDS_ADR = "needs_adr"


@dataclass(frozen=True)
class ConceptSignature:
    """Canonical semantic fingerprint for a concept."""

    name: str
    authority: str | None = None
    family: str | None = None
    knows: str | None = None
    owns: str | None = None
    purpose: str | None = None
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_terms(self) -> set[str]:
        terms: set[str] = set()

        def add(value: str | None) -> None:
            if value:
                for token in value.replace("_", " ").replace("-", " ").lower().split():
                    if len(token) > 2:
                        terms.add(token)

        add(self.name)
        add(self.authority)
        add(self.family)
        add(self.knows)
        add(self.owns)
        add(self.purpose)

        for alias in self.aliases:
            add(alias)
        for tag in self.tags:
            add(tag)

        return terms


@dataclass
class CollisionFinding:
    source: ConceptSignature
    target: ConceptSignature
    collision_type: CollisionType
    severity: CollisionSeverity
    confidence: float
    recommended_outcome: CollisionOutcome
    rationale: str
    requires_adr: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class CollisionReport:
    candidate: ConceptSignature
    findings: list[CollisionFinding] = field(default_factory=list)
    passed: bool = True
    summary: str = "No collision detected."
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def add_finding(self, finding: CollisionFinding) -> None:
        self.findings.append(finding)
        if finding.severity in {
            CollisionSeverity.OVERLAP_RISK,
            CollisionSeverity.COLLISION_RISK,
            CollisionSeverity.VIOLATION,
        }:
            self.passed = False
            self.summary = "Collision review required."

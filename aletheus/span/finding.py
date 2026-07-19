"""Unified finding model for SPAN™ analyzers.

A finding is a normalized architectural conclusion produced by one analyzer
from one or more evidence records. Findings are immutable enough for safe
reporting, serialization, correlation, and future governance evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any, Iterable, Mapping
import json


class Severity(str, Enum):
    """Normalized SPAN finding severity."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def weight(self) -> int:
        return {
            Severity.INFO: 0,
            Severity.LOW: 1,
            Severity.MEDIUM: 3,
            Severity.HIGH: 7,
            Severity.CRITICAL: 12,
        }[self]


@dataclass(frozen=True, slots=True)
class Finding:
    """A normalized architectural observation or governance concern."""

    analyzer: str
    category: str
    title: str
    summary: str
    severity: Severity = Severity.INFO
    confidence: float = 1.0
    recommendation: str | None = None
    evidence_ids: tuple[str, ...] = ()
    owner: str | None = None
    tags: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    finding_id: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if not self.analyzer.strip():
            raise ValueError("analyzer cannot be empty")
        if not self.category.strip():
            raise ValueError("category cannot be empty")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.summary.strip():
            raise ValueError("summary cannot be empty")

        object.__setattr__(self, "evidence_ids", tuple(dict.fromkeys(self.evidence_ids)))
        object.__setattr__(self, "tags", tuple(dict.fromkeys(self.tags)))

        if not self.finding_id:
            payload = {
                "analyzer": self.analyzer,
                "category": self.category,
                "title": self.title,
                "summary": self.summary,
                "evidence_ids": self.evidence_ids,
            }
            digest = sha256(
                json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:20]
            object.__setattr__(self, "finding_id", f"finding:{digest}")

    @property
    def risk_score(self) -> float:
        """Return a confidence-adjusted severity score."""

        return round(self.severity.weight * self.confidence, 4)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "analyzer": self.analyzer,
            "category": self.category,
            "title": self.title,
            "summary": self.summary,
            "severity": self.severity.value,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "recommendation": self.recommendation,
            "evidence_ids": list(self.evidence_ids),
            "owner": self.owner,
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Finding":
        return cls(
            finding_id=str(payload.get("finding_id", "")),
            analyzer=str(payload["analyzer"]),
            category=str(payload["category"]),
            title=str(payload["title"]),
            summary=str(payload["summary"]),
            severity=Severity(str(payload.get("severity", Severity.INFO.value))),
            confidence=float(payload.get("confidence", 1.0)),
            recommendation=payload.get("recommendation"),
            evidence_ids=tuple(str(value) for value in payload.get("evidence_ids", ())),
            owner=payload.get("owner"),
            tags=tuple(str(value) for value in payload.get("tags", ())),
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass(slots=True)
class FindingSet:
    """Mutable collection used during analyzer and pipeline execution."""

    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        if all(item.finding_id != finding.finding_id for item in self.findings):
            self.findings.append(finding)

    def extend(self, findings: Iterable[Finding]) -> None:
        for finding in findings:
            self.add(finding)

    def by_severity(self, severity: Severity) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity is severity)

    def by_category(self, category: str) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.category == category)

    @property
    def total_risk(self) -> float:
        return round(sum(item.risk_score for item in self.findings), 4)

    def to_list(self) -> list[dict[str, Any]]:
        return [finding.to_dict() for finding in self.findings]

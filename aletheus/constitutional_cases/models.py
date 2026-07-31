"""Canonical Constitutional Case models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_case_id() -> str:
    return f"CASE-{uuid4().hex[:12].upper()}"


class CaseStatus(StrEnum):
    DETECTED = "detected"
    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RECOVERING = "recovering"
    RESOLVED = "resolved"
    VERIFIED = "verified"
    CLOSED = "closed"
    ARCHIVED = "archived"


class CaseSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CaseCriticality(StrEnum):
    SUPPORTING = "supporting"
    IMPORTANT = "important"
    CRITICAL = "critical"
    CONSTITUTIONAL = "constitutional"


@dataclass(frozen=True, slots=True)
class CaseContract:
    case_type: str
    purpose: str

    permitted_mission_types: tuple[str, ...]
    required_institutions: tuple[str, ...]
    required_evidence_types: tuple[str, ...]
    closure_criteria: tuple[str, ...]

    governance_required: bool = False
    council_required_on_critical: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ConstitutionalCase:
    case_id: str
    case_type: str
    canonical_name: str
    purpose: str
    authority: str
    jurisdiction: str
    contract: CaseContract

    status: CaseStatus = CaseStatus.DETECTED
    severity: CaseSeverity = CaseSeverity.MEDIUM
    criticality: CaseCriticality = CaseCriticality.IMPORTANT

    correlation_id: str = ""

    mission_ids: list[str] = field(default_factory=list)
    participating_institutions: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)
    governance_records: list[dict[str, Any]] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    created_at: str = field(default_factory=_timestamp)
    opened_at: str | None = None
    resolved_at: str | None = None
    verified_at: str | None = None
    closed_at: str | None = None

    genesis: str = "52"
    version: str = "0.1.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.correlation_id:
            self.correlation_id = self.case_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_type": self.case_type,
            "canonical_name": self.canonical_name,
            "purpose": self.purpose,
            "authority": self.authority,
            "jurisdiction": self.jurisdiction,
            "contract": self.contract.to_dict(),
            "status": self.status.value,
            "severity": self.severity.value,
            "criticality": self.criticality.value,
            "correlation_id": self.correlation_id,
            "mission_ids": list(self.mission_ids),
            "participating_institutions": list(self.participating_institutions),
            "evidence": list(self.evidence),
            "event_ids": list(self.event_ids),
            "governance_records": list(self.governance_records),
            "failures": list(self.failures),
            "created_at": self.created_at,
            "opened_at": self.opened_at,
            "resolved_at": self.resolved_at,
            "verified_at": self.verified_at,
            "closed_at": self.closed_at,
            "genesis": self.genesis,
            "version": self.version,
            "metadata": dict(self.metadata),
        }

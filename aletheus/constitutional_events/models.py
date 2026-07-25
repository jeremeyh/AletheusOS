"""Canonical event models for the AletheusOS Constitutional Event Fabric."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_event_id() -> str:
    return f"CEV-{uuid4().hex[:12].upper()}"


class ConstitutionalEventType(StrEnum):
    """Initial canonical constitutional event vocabulary."""

    CIVILIZATION_BOOTSTRAP_STARTED = "CivilizationBootstrapStarted"
    CIVILIZATION_BOOTSTRAP_COMPLETED = "CivilizationBootstrapCompleted"

    INSTITUTION_ESTABLISHED = "InstitutionEstablished"
    INSTITUTION_PROJECTED = "InstitutionProjected"
    INSTITUTION_HEALTH_CHANGED = "InstitutionHealthChanged"

    WATCH_TOWER_ASSESSMENT_REQUESTED = "WatchTowerAssessmentRequested"
    WATCH_TOWER_ASSESSMENT_COMPLETED = "WatchTowerAssessmentCompleted"
    INTEGRITY_FINDING_CREATED = "IntegrityFindingCreated"

    PLATFORM_ASSESSMENT_REQUESTED = "PlatformAssessmentRequested"
    PLATFORM_ASSESSMENT_COMPLETED = "PlatformAssessmentCompleted"

    COUNCIL_REVIEW_REQUESTED = "CouncilReviewRequested"
    COUNCIL_DECISION_RECORDED = "CouncilDecisionRecorded"

    HOMEOSTASIS_UPDATED = "HomeostasisUpdated"
    SYNTHETIC_HARMONY_CHANGED = "SyntheticHarmonyChanged"

    LEDGER_ENTRY_CREATED = "LedgerEntryCreated"


@dataclass(frozen=True, slots=True)
class ConstitutionalEvent:
    """
    Immutable fact communicated between constitutional institutions.

    The event contains identity, causality, evidence, and version context so
    Ledger and Time Travel™ can reconstruct how the civilization evolved.
    """

    event_id: str
    event_type: ConstitutionalEventType
    source_identity: str
    effective_at: str

    payload: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[dict[str, Any], ...] = ()
    tags: tuple[str, ...] = ()

    correlation_id: str | None = None
    causation_id: str | None = None

    certified: bool = False
    constitution_version: str = "0.1.0"
    genesis_version: str = "12"

    recorded_at: str = field(default_factory=_timestamp)

    @classmethod
    def create(
        cls,
        event_type: ConstitutionalEventType,
        source_identity: str,
        *,
        payload: dict[str, Any] | None = None,
        evidence: tuple[dict[str, Any], ...] = (),
        tags: tuple[str, ...] = (),
        correlation_id: str | None = None,
        causation_id: str | None = None,
        certified: bool = False,
        effective_at: str | None = None,
        constitution_version: str = "0.1.0",
        genesis_version: str = "12",
    ) -> ConstitutionalEvent:
        return cls(
            event_id=new_event_id(),
            event_type=event_type,
            source_identity=source_identity,
            effective_at=effective_at or _timestamp(),
            payload=payload or {},
            evidence=evidence,
            tags=tags,
            correlation_id=correlation_id,
            causation_id=causation_id,
            certified=certified,
            constitution_version=constitution_version,
            genesis_version=genesis_version,
        )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["event_type"] = self.event_type.value
        return value

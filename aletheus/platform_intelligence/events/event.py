"""Immutable ConstitutionalEvent envelope."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
)

from .enums import (
    ConstitutionalEventKind,
    ConstitutionalEventSeverity,
)
from .exceptions import ConstitutionalEventValidationError


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _freeze_mapping(
    value: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True, slots=True)
class ConstitutionalEvent:
    """
    Immutable constitutional fact emitted by AletheusOS.

    Events describe what happened. They do not execute behavior, mutate
    platform state, or depend on a particular event transport.
    """

    event_id: UUID
    kind: ConstitutionalEventKind
    source: ConstitutionalAddress
    subject: ConstitutionalAddress
    occurred_at: datetime

    severity: ConstitutionalEventSeverity = (
        ConstitutionalEventSeverity.INFO
    )

    correlation_id: UUID = field(default_factory=uuid4)
    causation_id: UUID | None = None

    sequence: int | None = None
    schema_version: str = "1.0"

    payload: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    metadata: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if self.occurred_at.tzinfo is None:
            raise ConstitutionalEventValidationError(
                "occurred_at must include timezone information."
            )

        if self.sequence is not None and self.sequence < 0:
            raise ConstitutionalEventValidationError(
                "Event sequence cannot be negative."
            )

        if not self.schema_version.strip():
            raise ConstitutionalEventValidationError(
                "schema_version cannot be empty."
            )

        object.__setattr__(
            self,
            "occurred_at",
            self.occurred_at.astimezone(UTC),
        )
        object.__setattr__(
            self,
            "schema_version",
            self.schema_version.strip(),
        )
        object.__setattr__(
            self,
            "payload",
            _freeze_mapping(self.payload),
        )
        object.__setattr__(
            self,
            "metadata",
            _freeze_mapping(self.metadata),
        )

    @classmethod
    def create(
        cls,
        *,
        kind: ConstitutionalEventKind,
        source: str | ConstitutionalAddress,
        subject: str | ConstitutionalAddress,
        severity: ConstitutionalEventSeverity = (
            ConstitutionalEventSeverity.INFO
        ),
        payload: Mapping[str, Any] | None = None,
        metadata: Mapping[str, Any] | None = None,
        correlation_id: UUID | None = None,
        causation_id: UUID | None = None,
        sequence: int | None = None,
        schema_version: str = "1.0",
        event_id: UUID | None = None,
        occurred_at: datetime | None = None,
    ) -> ConstitutionalEvent:
        return cls(
            event_id=event_id or uuid4(),
            kind=kind,
            source=(
                source
                if isinstance(source, ConstitutionalAddress)
                else ConstitutionalAddress(source)
            ),
            subject=(
                subject
                if isinstance(subject, ConstitutionalAddress)
                else ConstitutionalAddress(subject)
            ),
            occurred_at=occurred_at or _utc_now(),
            severity=severity,
            correlation_id=correlation_id or uuid4(),
            causation_id=causation_id,
            sequence=sequence,
            schema_version=schema_version,
            payload=_freeze_mapping(payload),
            metadata=_freeze_mapping(metadata),
        )

    def with_sequence(
        self,
        sequence: int,
    ) -> ConstitutionalEvent:
        """Return a sequenced copy without mutating the original event."""

        if sequence < 0:
            raise ConstitutionalEventValidationError(
                "Event sequence cannot be negative."
            )

        return replace(
            self,
            sequence=sequence,
        )

    def caused_by(
        self,
        event: ConstitutionalEvent,
    ) -> ConstitutionalEvent:
        """Return a copy causally linked to another event."""

        return replace(
            self,
            causation_id=event.event_id,
            correlation_id=event.correlation_id,
        )

    def integrity_hash(self) -> str:
        """Return a deterministic digest of the constitutional event."""

        payload = {
            "event_id": str(self.event_id),
            "kind": self.kind.value,
            "source": str(self.source),
            "subject": str(self.subject),
            "occurred_at": self.occurred_at.isoformat(),
            "severity": self.severity.value,
            "correlation_id": str(self.correlation_id),
            "causation_id": (
                str(self.causation_id)
                if self.causation_id is not None
                else None
            ),
            "sequence": self.sequence,
            "schema_version": self.schema_version,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def to_envelope(self) -> dict[str, Any]:
        """Serialize the event into a transport-neutral envelope."""

        return {
            "event_id": str(self.event_id),
            "kind": self.kind.value,
            "source": str(self.source),
            "subject": str(self.subject),
            "occurred_at": self.occurred_at.isoformat(),
            "severity": self.severity.value,
            "correlation_id": str(self.correlation_id),
            "causation_id": (
                str(self.causation_id)
                if self.causation_id is not None
                else None
            ),
            "sequence": self.sequence,
            "schema_version": self.schema_version,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
            "integrity_hash": self.integrity_hash(),
        }

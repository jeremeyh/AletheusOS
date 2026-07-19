"""Institutional event records for the Constitutional Ledger."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(UTC).isoformat()


def new_institutional_event_id() -> str:
    return f"ILE-{uuid4().hex[:12].upper()}"


@dataclass(frozen=True, slots=True)
class InstitutionalLedgerEvent:
    """
    Authoritative historical record of an institutional event.

    effective_at:
        When the event occurred or became true.

    recorded_at:
        When Ledger received and recorded the event.

    Keeping both values establishes the initial bitemporal foundation
    required by Time Travel™.
    """

    event_id: str
    event_type: str
    source_identity: str
    effective_at: str
    recorded_at: str = field(default_factory=_timestamp)

    payload: dict[str, Any] = field(default_factory=dict)
    evidence: tuple[dict[str, Any], ...] = ()
    tags: tuple[str, ...] = ()

    correlation_id: str | None = None
    causation_id: str | None = None
    supersedes: str | None = None

    certified: bool = False
    constitution_version: str = "0.1.0"
    genesis_version: str = "12"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

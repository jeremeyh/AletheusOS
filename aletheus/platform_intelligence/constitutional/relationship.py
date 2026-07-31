"""Typed constitutional relationships."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4

from .enums import RelationshipKind
from .identity import ConstitutionalAddress


def _utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class ConstitutionalRelationship:
    """A semantic directed edge between two constitutional objects."""

    source: ConstitutionalAddress
    target: ConstitutionalAddress
    kind: RelationshipKind
    relationship_id: UUID
    created_at: datetime
    metadata: Mapping[str, Any]

    @classmethod
    def create(
        cls,
        *,
        source: str | ConstitutionalAddress,
        target: str | ConstitutionalAddress,
        kind: RelationshipKind,
        metadata: Mapping[str, Any] | None = None,
        relationship_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> ConstitutionalRelationship:
        source_address = (
            source
            if isinstance(source, ConstitutionalAddress)
            else ConstitutionalAddress(source)
        )
        target_address = (
            target
            if isinstance(target, ConstitutionalAddress)
            else ConstitutionalAddress(target)
        )

        if source_address == target_address:
            raise ValueError("A constitutional relationship cannot target itself.")

        return cls(
            source=source_address,
            target=target_address,
            kind=kind,
            relationship_id=relationship_id or uuid4(),
            created_at=created_at or _utc_now(),
            metadata=MappingProxyType(dict(metadata or {})),
        )

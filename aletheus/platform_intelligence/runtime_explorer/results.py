"""Immutable Runtime Explorer result models."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalObject,
)


@dataclass(frozen=True, slots=True)
class ExplorerSearchResult:
    """One ranked constitutional search result."""

    object: ConstitutionalObject
    score: int
    matched_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "object": self.object.to_snapshot(),
            "score": self.score,
            "matched_fields": list(
                self.matched_fields
            ),
        }


@dataclass(frozen=True, slots=True)
class ExplorerImpactResult:
    """Blast-radius projection for a constitutional object."""

    subject: ConstitutionalObject
    direct_dependents: tuple[
        ConstitutionalObject,
        ...,
    ]
    transitive_dependents: tuple[
        ConstitutionalObject,
        ...,
    ]
    affected_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject.to_snapshot(),
            "direct_dependents": [
                item.to_snapshot()
                for item in self.direct_dependents
            ],
            "transitive_dependents": [
                item.to_snapshot()
                for item
                in self.transitive_dependents
            ],
            "affected_count": self.affected_count,
        }


@dataclass(frozen=True, slots=True)
class RuntimeExplorerStatistics:
    """Immutable Runtime Explorer statistics."""

    objects: int
    services: int
    relationships: int
    unhealthy: int
    orphans: int
    cycles: int
    retained_snapshots: int
    twin_revision: int
    objects_by_kind: Mapping[str, int]
    objects_by_state: Mapping[str, int]
    objects_by_health: Mapping[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "objects": self.objects,
            "services": self.services,
            "relationships": self.relationships,
            "unhealthy": self.unhealthy,
            "orphans": self.orphans,
            "cycles": self.cycles,
            "retained_snapshots": (
                self.retained_snapshots
            ),
            "twin_revision": self.twin_revision,
            "objects_by_kind": dict(
                self.objects_by_kind
            ),
            "objects_by_state": dict(
                self.objects_by_state
            ),
            "objects_by_health": dict(
                self.objects_by_health
            ),
        }

"""Immutable Platform Digital Twin snapshots."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from uuid import UUID, uuid4


def _freeze_mapping(
    value: Mapping[str, Any],
) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class TwinSnapshot:
    """Immutable point-in-time representation of AletheusOS."""

    snapshot_id: UUID
    revision: int
    created_at: datetime
    services: tuple[Mapping[str, Any], ...]
    nodes: tuple[Mapping[str, Any], ...]
    relationships: tuple[Mapping[str, Any], ...]
    health: Mapping[str, Any]
    topology: Mapping[str, Any]
    statistics: Mapping[str, Any]
    last_event: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        if self.revision < 0:
            raise ValueError(
                "Snapshot revision cannot be negative."
            )

        if self.created_at.tzinfo is None:
            raise ValueError(
                "Snapshot timestamp must include timezone."
            )

        object.__setattr__(
            self,
            "created_at",
            self.created_at.astimezone(UTC),
        )
        object.__setattr__(
            self,
            "services",
            tuple(
                _freeze_mapping(item)
                for item in self.services
            ),
        )
        object.__setattr__(
            self,
            "nodes",
            tuple(
                _freeze_mapping(item)
                for item in self.nodes
            ),
        )
        object.__setattr__(
            self,
            "relationships",
            tuple(
                _freeze_mapping(item)
                for item in self.relationships
            ),
        )
        object.__setattr__(
            self,
            "health",
            _freeze_mapping(self.health),
        )
        object.__setattr__(
            self,
            "topology",
            _freeze_mapping(self.topology),
        )
        object.__setattr__(
            self,
            "statistics",
            _freeze_mapping(self.statistics),
        )

        if self.last_event is not None:
            object.__setattr__(
                self,
                "last_event",
                _freeze_mapping(self.last_event),
            )

    @classmethod
    def create(
        cls,
        *,
        revision: int,
        services: tuple[Mapping[str, Any], ...],
        nodes: tuple[Mapping[str, Any], ...],
        relationships: tuple[Mapping[str, Any], ...],
        health: Mapping[str, Any],
        topology: Mapping[str, Any],
        statistics: Mapping[str, Any],
        last_event: Mapping[str, Any] | None = None,
        snapshot_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> TwinSnapshot:
        return cls(
            snapshot_id=snapshot_id or uuid4(),
            revision=revision,
            created_at=created_at or datetime.now(UTC),
            services=services,
            nodes=nodes,
            relationships=relationships,
            health=health,
            topology=topology,
            statistics=statistics,
            last_event=last_event,
        )

    def integrity_hash(self) -> str:
        """Return a deterministic snapshot digest."""

        payload = {
            "revision": self.revision,
            "services": [
                dict(item)
                for item in self.services
            ],
            "nodes": [
                dict(item)
                for item in self.nodes
            ],
            "relationships": [
                dict(item)
                for item in self.relationships
            ],
            "health": dict(self.health),
            "topology": dict(self.topology),
            "statistics": dict(self.statistics),
            "last_event": (
                dict(self.last_event)
                if self.last_event is not None
                else None
            ),
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": str(self.snapshot_id),
            "revision": self.revision,
            "created_at": self.created_at.isoformat(),
            "services": [
                dict(item)
                for item in self.services
            ],
            "nodes": [
                dict(item)
                for item in self.nodes
            ],
            "relationships": [
                dict(item)
                for item in self.relationships
            ],
            "health": dict(self.health),
            "topology": dict(self.topology),
            "statistics": dict(self.statistics),
            "last_event": (
                dict(self.last_event)
                if self.last_event is not None
                else None
            ),
            "integrity_hash": self.integrity_hash(),
        }

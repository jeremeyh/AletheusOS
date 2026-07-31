"""Models for the Kinekt™ Architectural Digital Twin."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class TwinNode:
    node_id: str
    node_type: str
    name: str
    attributes: dict[str, Any]
    provenance: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TwinRelationship:
    source: str
    target: str
    relationship: str
    attributes: dict[str, Any]
    provenance: tuple[str, ...] = ()


@dataclass(slots=True)
class TwinSnapshot:
    generated_at: str
    snapshot_id: str
    repository_commit: str
    nodes: list[TwinNode] = field(default_factory=list)
    relationships: list[TwinRelationship] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, str] = field(default_factory=dict)
    changes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

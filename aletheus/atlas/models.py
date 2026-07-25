from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class AtlasNodeType(str, Enum):
    AUTHORITY = "authority"
    FAMILY = "family"
    SUBSYSTEM = "subsystem"
    SERVICE = "service"
    ENGINE = "engine"
    REGISTRY = "registry"
    FABRIC = "fabric"
    CIRCUIT = "circuit"
    RUNTIME = "runtime"
    MEMORY = "memory"
    GOVERNANCE = "governance"
    SECURITY = "security"
    APPLICATION = "application"
    UNKNOWN = "unknown"


class AtlasEdgeType(str, Enum):
    OWNS = "owns"
    KNOWS = "knows"
    DEPENDS_ON = "depends_on"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    BELONGS_TO = "belongs_to"
    OBSERVES = "observes"
    VALIDATES = "validates"
    ROUTES_TO = "routes_to"
    REGISTERS_WITH = "registers_with"
    COLLABORATES_WITH = "collaborates_with"


@dataclass(frozen=True)
class AtlasNode:
    id: str
    name: str
    type: AtlasNodeType = AtlasNodeType.UNKNOWN
    authority: str | None = None
    family: str | None = None
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AtlasEdge:
    source_id: str
    target_id: str
    type: AtlasEdgeType
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchitectureGraph:
    nodes: dict[str, AtlasNode] = field(default_factory=dict)
    edges: list[AtlasEdge] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def add_node(self, node: AtlasNode) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: AtlasEdge) -> None:
        self.edges.append(edge)

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        return len(self.edges)


@dataclass
class TopologySnapshot:
    graph: ArchitectureGraph
    subsystem_count: int
    authority_count: int
    family_count: int
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class AtlasReport:
    snapshot: TopologySnapshot
    findings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

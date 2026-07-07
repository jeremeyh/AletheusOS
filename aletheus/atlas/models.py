from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


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
    authority: Optional[str] = None
    family: Optional[str] = None
    path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AtlasEdge:
    source_id: str
    target_id: str
    type: AtlasEdgeType
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchitectureGraph:
    nodes: Dict[str, AtlasNode] = field(default_factory=dict)
    edges: List[AtlasEdge] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

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
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AtlasReport:
    snapshot: TopologySnapshot
    findings: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

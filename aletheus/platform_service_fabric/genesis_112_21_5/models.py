from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Tuple

PREDECESSOR_EVIDENCE_DIGEST = "sha256:96b20ef5c07c959db9b25cd2d98c191460a187ad41ef9c57a5d5979f344474ea"
PREDECESSOR_MESH_DIGEST = "sha256:9a3d2d432d88c72ba92cc5b0fed3c224ff50e9cf001ad2c5cbcd25f8cd8f65bb"

class TopologyClassification(str, Enum):
    CANONICAL = "CANONICAL"
    BOUNDED_EXTERNAL = "BOUNDED_EXTERNAL"
    DORMANT = "DORMANT"
    ORPHANED = "ORPHANED"
    CONFLICTING = "CONFLICTING"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class TopologyNode:
    node_id: str
    owner_domain: str
    implementation_ref: str
    capabilities: Tuple[str, ...] = field(default_factory=tuple)
    lifecycle_authority: str = ""
    reliability_authority: str = "RSF"
    persistence_authority: str = "MAMMOTH"
    release_authority: str = "RAF"

@dataclass(frozen=True)
class TopologyEdge:
    source: str
    target: str
    relation: str
    authority: str

@dataclass(frozen=True)
class TopologyFinding:
    subject: str
    classification: TopologyClassification
    reason: str

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ConstitutionalState:
    veracity: float
    consensus: float
    crypto: float
    provenance: float
    entropy: float
    risk: float
    freshness: float
    priority: float
    cognitive_load: float
    confidence: float

    def bounded(self) -> ConstitutionalState:
        return ConstitutionalState(
            **{key: min(1.0, max(0.0, value)) for key, value in asdict(self).items()}
        )


@dataclass(frozen=True)
class ProjectionNode:
    node_id: str
    node_type: str
    state: ConstitutionalState
    props: dict[str, Any] = field(default_factory=dict)
    children: tuple[ProjectionNode, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodeId": self.node_id,
            "type": self.node_type,
            "state": asdict(self.state),
            "props": self.props,
            "children": [child.to_dict() for child in self.children],
        }

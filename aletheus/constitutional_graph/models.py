from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp():
    return datetime.now(UTC).isoformat()


def new_node_id():
    return f"NODE-{uuid4().hex[:12].upper()}"


def new_edge_id():
    return f"EDGE-{uuid4().hex[:12].upper()}"


@dataclass(slots=True)
class GraphNode:
    node_id: str
    node_type: str
    label: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "data": self.data,
            "timestamp": self.timestamp,
        }


@dataclass(slots=True)
class GraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relationship: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relationship": self.relationship,
            "data": self.data,
            "timestamp": self.timestamp,
        }

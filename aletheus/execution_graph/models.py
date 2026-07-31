"""
AletheusOS
Genesis 50.0

Foundation Execution Graph™

Canonical Graph Models
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_node_id() -> str:
    return f"NODE-{uuid4().hex[:12].upper()}"


def new_edge_id() -> str:
    return f"EDGE-{uuid4().hex[:12].upper()}"


class NodeType(StrEnum):
    INTENT = "INTENT"

    IDENTITY = "IDENTITY"

    MEMORY = "MEMORY"

    REASON = "REASON"

    EVIDENCE = "EVIDENCE"

    EXECUTION = "EXECUTION"

    COUNCIL = "COUNCIL"

    APPLICATION = "APPLICATION"

    ORGANIZATION = "ORGANIZATION"


class EdgeType(StrEnum):
    GENERATED = "GENERATED"

    USED = "USED"

    REFERENCED = "REFERENCED"

    CREATED = "CREATED"

    PRODUCED = "PRODUCED"

    JUSTIFIED_BY = "JUSTIFIED_BY"

    EVALUATED_BY = "EVALUATED_BY"

    STORED_IN = "STORED_IN"

    BELONGS_TO = "BELONGS_TO"

    EXECUTED_BY = "EXECUTED_BY"


@dataclass(slots=True)
class GraphNode:
    node_id: str

    node_type: NodeType

    canonical_id: str

    display_name: str

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)


@dataclass(slots=True)
class GraphEdge:
    edge_id: str

    source: str

    target: str

    edge_type: EdgeType

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:

        return asdict(self)

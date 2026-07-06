from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class UCINodeType(str, Enum):
    INTENT = "intent"
    MEMORY = "memory"
    KNOWLEDGE = "knowledge"
    DECISION = "decision"
    EVIDENCE = "evidence"
    EXECUTION = "execution"
    POLICY = "policy"
    GOVERNANCE = "governance"
    SERVICE = "service"
    ENGINE = "engine"
    APPLICATION = "application"
    PLATFORM_COMPONENT = "platform_component"
    HEALTH_SIGNAL = "health_signal"
    OUTCOME = "outcome"
    UNKNOWN = "unknown"


class UCIRelationshipType(str, Enum):
    DERIVED_FROM = "derived_from"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    DEPENDS_ON = "depends_on"
    PRODUCED_BY = "produced_by"
    CONSUMED_BY = "consumed_by"
    GOVERNED_BY = "governed_by"
    VALIDATED_BY = "validated_by"
    SUPERSEDES = "supersedes"
    RELATES_TO = "relates_to"
    TRIGGERED = "triggered"
    RESULTED_IN = "resulted_in"


@dataclass
class UCINode:
    """
    A cognitive object indexed by the Unified Cognitive Index.

    The UCI does not own the source object.
    It indexes identity, context, lineage, evidence, and relationships.
    """

    node_id: str
    node_type: UCINodeType
    title: str
    description: str = ""
    source_system: str = "unknown"

    intent_id: Optional[str] = None
    steward: Optional[str] = None
    confidence: float = 1.0
    health: Optional[float] = None

    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class UCIRelationship:
    """
    A weighted cognitive relationship between two indexed nodes.
    """

    relationship_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: UCIRelationshipType

    weight: float = 1.0
    confidence: float = 1.0

    evidence_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class UCITrace:
    """
    A lineage or causality trace through the cognitive index.
    """

    origin_node_id: str
    terminal_node_id: str
    path: List[str]
    relationships: List[str] = field(default_factory=list)
    confidence: float = 1.0
    generated_at: str = field(default_factory=utc_now)


@dataclass
class UCIQueryResult:
    """
    Standard query response from the Unified Cognitive Index.
    """

    nodes: List[UCINode] = field(default_factory=list)
    relationships: List[UCIRelationship] = field(default_factory=list)
    total_nodes: int = 0
    total_relationships: int = 0
    generated_at: str = field(default_factory=utc_now)


@dataclass
class UCIHealthReport:
    """
    Health summary for the Unified Cognitive Index.
    """

    status: str
    node_count: int
    relationship_count: int
    orphan_node_count: int
    average_relationship_weight: float
    generated_at: str = field(default_factory=utc_now)

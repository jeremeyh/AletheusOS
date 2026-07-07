from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class OntologyEntityType(str, Enum):
    """Canonical entity categories for the AletheusOS Ontology."""

    AUTHORITY = "authority"
    FAMILY = "family"
    PRINCIPLE = "principle"
    ADR = "adr"
    SUBSYSTEM = "subsystem"
    CAPABILITY = "capability"
    SERVICE = "service"
    ENGINE = "engine"
    REGISTRY = "registry"
    CIRCUIT = "circuit"
    FABRIC = "fabric"
    MESH = "mesh"
    GRAPH = "graph"
    ENVELOPE = "envelope"
    MODULE = "module"
    APPLICATION = "application"
    INFRASTRUCTURE = "infrastructure"
    CONCEPT = "concept"
    UNKNOWN = "unknown"


class OntologyStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    CANONICAL = "canonical"
    SUPERSEDED = "superseded"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    HISTORICAL = "historical"
    UNKNOWN = "unknown"


class RelationshipType(str, Enum):
    OWNS = "owns"
    KNOWS = "knows"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    ROUTES_TO = "routes_to"
    SUPERVISES = "supervises"
    GOVERNS = "governs"
    OBSERVES = "observes"
    VALIDATES = "validates"
    ARCHIVES = "archives"
    SUPERSEDES = "supersedes"
    BELONGS_TO = "belongs_to"
    COLLIDES_WITH = "collides_with"
    GENERATES = "generates"
    PROTECTS = "protects"
    STABILIZES = "stabilizes"
    INFLUENCES = "influences"
    RELATES_TO = "relates_to"


class CollisionSeverity(str, Enum):
    UNIQUE = "unique"
    ADJACENT = "adjacent"
    OVERLAP_RISK = "overlap_risk"
    COLLISION_RISK = "collision_risk"
    VIOLATION = "violation"


@dataclass
class OntologyEntity:
    """
    Canonical semantic identity for any AletheusOS concept.

    The Ontology gives each authority, subsystem, principle, ADR,
    capability, service, registry, circuit, fabric, mesh, or module
    a permanent identity before it becomes part of the Super-Mesh.
    """

    entity_id: str
    name: str
    entity_type: OntologyEntityType
    description: str = ""
    status: OntologyStatus = OntologyStatus.PROPOSED

    family: Optional[str] = None
    authority: Optional[str] = None
    authority_sentence: Optional[str] = None
    genesis: Optional[str] = None

    aliases: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class OntologyRelationship:
    """Typed semantic edge between two ontology entities."""

    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType

    description: str = ""
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class ConceptCollision:
    """A possible semantic, functional, structural, authority, or historical overlap."""

    collision_id: str
    source_entity_id: str
    target_entity_id: str
    severity: CollisionSeverity
    collision_type: str
    summary: str

    recommendation: str = "review"
    status: OntologyStatus = OntologyStatus.PROPOSED
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class OntologyLineage:
    """Concept genealogy: what superseded, replaced, split, merged, or archived what."""

    lineage_id: str
    entity_id: str
    predecessor_ids: List[str] = field(default_factory=list)
    successor_ids: List[str] = field(default_factory=list)
    superseded_by: Optional[str] = None
    archived_reason: Optional[str] = None
    migration_status: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class OntologyQueryResult:
    entities: List[OntologyEntity] = field(default_factory=list)
    relationships: List[OntologyRelationship] = field(default_factory=list)
    collisions: List[ConceptCollision] = field(default_factory=list)
    total_entities: int = 0
    total_relationships: int = 0
    total_collisions: int = 0
    generated_at: str = field(default_factory=utc_now)


@dataclass
class OntologyHealthReport:
    status: str
    entity_count: int
    relationship_count: int
    collision_count: int
    orphan_entity_count: int
    canonical_entity_count: int
    generated_at: str = field(default_factory=utc_now)

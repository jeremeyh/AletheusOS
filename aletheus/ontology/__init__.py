"""AletheusOS Ontology Core.

The Ontology is the canonical semantic backbone of the Super-Mesh.
It gives every architectural identity a permanent semantic record,
relationships, lineage, status, and collision visibility.
"""

from .models import (
    CollisionSeverity,
    ConceptCollision,
    OntologyEntity,
    OntologyEntityType,
    OntologyHealthReport,
    OntologyLineage,
    OntologyQueryResult,
    OntologyRelationship,
    OntologyStatus,
    RelationshipType,
)
from .registry import OntologyRegistry, ontology_registry
from .resolver import OntologyResolver
from .service import OntologyService, ontology_service
from .validator import OntologyValidationResult, OntologyValidator

__all__ = [
    "CollisionSeverity",
    "ConceptCollision",
    "OntologyEntity",
    "OntologyEntityType",
    "OntologyHealthReport",
    "OntologyLineage",
    "OntologyQueryResult",
    "OntologyRelationship",
    "OntologyRegistry",
    "OntologyResolver",
    "OntologyService",
    "OntologyStatus",
    "OntologyValidationResult",
    "OntologyValidator",
    "RelationshipType",
    "ontology_registry",
    "ontology_service",
]

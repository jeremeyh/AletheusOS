from __future__ import annotations

from .models import (
    ConceptCollision,
    OntologyEntity,
    OntologyHealthReport,
    OntologyLineage,
    OntologyQueryResult,
    OntologyRelationship,
    OntologyStatus,
    RelationshipType,
)


class OntologyRegistry:
    """
    In-memory canonical ontology registry for AletheusOS.

    The Ontology is the semantic backbone of the Super-Mesh. It records
    identity, authority, lineage, relationships, and collision signals.
    It does not govern or execute; it describes the platform so other
    authorities can reason consistently.
    """

    def __init__(self) -> None:
        self._entities: dict[str, OntologyEntity] = {}
        self._relationships: dict[str, OntologyRelationship] = {}
        self._collisions: dict[str, ConceptCollision] = {}
        self._lineage: dict[str, OntologyLineage] = {}

    # ---------------------------------------------------------
    # Entity Operations
    # ---------------------------------------------------------

    def register_entity(self, entity: OntologyEntity) -> None:
        self._entities[entity.entity_id] = entity

    def get_entity(self, entity_id: str) -> OntologyEntity | None:
        return self._entities.get(entity_id)

    def remove_entity(self, entity_id: str) -> None:
        self._entities.pop(entity_id, None)

    def all_entities(self) -> list[OntologyEntity]:
        return list(self._entities.values())

    def canonical_entities(self) -> list[OntologyEntity]:
        return [
            entity
            for entity in self._entities.values()
            if entity.status == OntologyStatus.CANONICAL
        ]

    # ---------------------------------------------------------
    # Relationship Operations
    # ---------------------------------------------------------

    def register_relationship(self, relationship: OntologyRelationship) -> None:
        self._relationships[relationship.relationship_id] = relationship

    def get_relationship(
        self,
        relationship_id: str,
    ) -> OntologyRelationship | None:
        return self._relationships.get(relationship_id)

    def all_relationships(self) -> list[OntologyRelationship]:
        return list(self._relationships.values())

    def outgoing_relationships(
        self,
        entity_id: str,
        relationship_type: RelationshipType | None = None,
    ) -> list[OntologyRelationship]:
        return [
            relationship
            for relationship in self._relationships.values()
            if relationship.source_entity_id == entity_id
            and (
                relationship_type is None
                or relationship.relationship_type == relationship_type
            )
        ]

    def incoming_relationships(
        self,
        entity_id: str,
        relationship_type: RelationshipType | None = None,
    ) -> list[OntologyRelationship]:
        return [
            relationship
            for relationship in self._relationships.values()
            if relationship.target_entity_id == entity_id
            and (
                relationship_type is None
                or relationship.relationship_type == relationship_type
            )
        ]

    def related_entities(
        self,
        entity_id: str,
    ) -> list[OntologyEntity]:
        related: list[OntologyEntity] = []

        for relationship in self.outgoing_relationships(entity_id):
            entity = self.get_entity(relationship.target_entity_id)
            if entity:
                related.append(entity)

        for relationship in self.incoming_relationships(entity_id):
            entity = self.get_entity(relationship.source_entity_id)
            if entity:
                related.append(entity)

        return related

    # ---------------------------------------------------------
    # Collision Operations
    # ---------------------------------------------------------

    def register_collision(self, collision: ConceptCollision) -> None:
        self._collisions[collision.collision_id] = collision

    def all_collisions(self) -> list[ConceptCollision]:
        return list(self._collisions.values())

    def collisions_for_entity(self, entity_id: str) -> list[ConceptCollision]:
        return [
            collision
            for collision in self._collisions.values()
            if collision.source_entity_id == entity_id
            or collision.target_entity_id == entity_id
        ]

    # ---------------------------------------------------------
    # Lineage Operations
    # ---------------------------------------------------------

    def register_lineage(self, lineage: OntologyLineage) -> None:
        self._lineage[lineage.lineage_id] = lineage

    def lineage_for_entity(self, entity_id: str) -> list[OntologyLineage]:
        return [
            lineage
            for lineage in self._lineage.values()
            if lineage.entity_id == entity_id
        ]

    # ---------------------------------------------------------
    # Query / Health
    # ---------------------------------------------------------

    def search(self, text: str) -> OntologyQueryResult:
        text = text.lower()

        entities = [
            entity
            for entity in self._entities.values()
            if text in entity.name.lower()
            or text in entity.description.lower()
            or any(text in alias.lower() for alias in entity.aliases)
            or any(text in tag.lower() for tag in entity.tags)
        ]

        return OntologyQueryResult(
            entities=entities,
            relationships=[],
            collisions=[],
            total_entities=len(entities),
            total_relationships=0,
            total_collisions=0,
        )

    def statistics(self) -> dict:
        return {
            "entities": len(self._entities),
            "relationships": len(self._relationships),
            "collisions": len(self._collisions),
            "lineage_records": len(self._lineage),
        }

    def health(self) -> OntologyHealthReport:
        orphan_count = 0

        for entity in self._entities.values():
            if not self.incoming_relationships(
                entity.entity_id
            ) and not self.outgoing_relationships(entity.entity_id):
                orphan_count += 1

        canonical_count = len(self.canonical_entities())

        status = "healthy"
        if self._entities and orphan_count == len(self._entities):
            status = "degraded"

        return OntologyHealthReport(
            status=status,
            entity_count=len(self._entities),
            relationship_count=len(self._relationships),
            collision_count=len(self._collisions),
            orphan_entity_count=orphan_count,
            canonical_entity_count=canonical_count,
        )


ontology_registry = OntologyRegistry()

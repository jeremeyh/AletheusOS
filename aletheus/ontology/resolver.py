from __future__ import annotations

from .models import OntologyEntity, RelationshipType
from .registry import OntologyRegistry, ontology_registry


class OntologyResolver:
    """Resolves canonical entities and relationship neighborhoods."""

    def __init__(self, registry: OntologyRegistry = ontology_registry) -> None:
        self.registry = registry

    def resolve_by_id(self, entity_id: str) -> OntologyEntity | None:
        return self.registry.get_entity(entity_id)

    def resolve_by_name(self, name: str) -> OntologyEntity | None:
        name_normalized = name.lower()
        for entity in self.registry.all_entities():
            if entity.name.lower() == name_normalized:
                return entity
            if any(alias.lower() == name_normalized for alias in entity.aliases):
                return entity
        return None

    def entities_owned_by(self, authority_id: str) -> list[OntologyEntity]:
        relationships = self.registry.outgoing_relationships(
            authority_id,
            RelationshipType.OWNS,
        )
        return [
            entity
            for relationship in relationships
            if (entity := self.registry.get_entity(relationship.target_entity_id))
        ]

    def owners_of(self, entity_id: str) -> list[OntologyEntity]:
        relationships = self.registry.incoming_relationships(
            entity_id,
            RelationshipType.OWNS,
        )
        return [
            entity
            for relationship in relationships
            if (entity := self.registry.get_entity(relationship.source_entity_id))
        ]

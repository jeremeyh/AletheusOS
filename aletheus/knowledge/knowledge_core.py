from __future__ import annotations

from typing import Any

from aletheus.knowledge.models import Entity, Relationship


class AletheusKnowledgeCore:
    def __init__(self) -> None:
        self.version = "0.6.0-genesis"
        self.entities: list[Entity] = []
        self.relationships: list[Relationship] = []

    def create_entity(
        self,
        label: str,
        entity_type: str = "generic",
        properties: dict[str, Any] | None = None,
    ) -> Entity:
        entity = Entity(
            label=label,
            entity_type=entity_type,
            properties=properties or {},
        )
        self.entities.append(entity)
        return entity

    def search_entities(
        self,
        label: str | None = None,
        entity_type: str | None = None,
    ) -> list[dict[str, Any]]:
        results = self.entities

        if label:
            needle = label.lower()
            results = [entity for entity in results if needle in entity.label.lower()]

        if entity_type:
            results = [entity for entity in results if entity.entity_type == entity_type]

        return [entity.to_dict() for entity in results]

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: dict[str, Any] | None = None,
    ) -> Relationship:
        relationship = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {},
        )
        self.relationships.append(relationship)
        return relationship

    def search_relationships(
        self,
        source_id: str | None = None,
        target_id: str | None = None,
        relationship_type: str | None = None,
    ) -> list[dict[str, Any]]:
        results = self.relationships

        if source_id:
            results = [item for item in results if item.source_id == source_id]

        if target_id:
            results = [item for item in results if item.target_id == target_id]

        if relationship_type:
            results = [item for item in results if item.relationship_type == relationship_type]

        return [item.to_dict() for item in results]

    def graph_export(self) -> dict[str, Any]:
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "relationships": [relationship.to_dict() for relationship in self.relationships],
        }

    def graph_query(self, entity_id: str) -> dict[str, Any]:
        entity = next((item for item in self.entities if item.entity_id == entity_id), None)

        outgoing = [
            item.to_dict()
            for item in self.relationships
            if item.source_id == entity_id
        ]

        incoming = [
            item.to_dict()
            for item in self.relationships
            if item.target_id == entity_id
        ]

        return {
            "entity": entity.to_dict() if entity else None,
            "outgoing": outgoing,
            "incoming": incoming,
        }

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}

        for entity in self.entities:
            by_type[entity.entity_type] = by_type.get(entity.entity_type, 0) + 1

        return {
            "version": self.version,
            "entities": len(self.entities),
            "relationships": len(self.relationships),
            "entities_by_type": by_type,
        }


knowledge_core = AletheusKnowledgeCore()

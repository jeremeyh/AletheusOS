"""
Graph Command Adapter

Genesis 7

Extracted from runtime/core.py
"""

from __future__ import annotations


class GraphCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def entity_create(self, context):

        payload = context.payload

        entity = self.runtime.knowledge.create_entity(
            label=payload.get(
                "label",
                "Untitled Entity",
            ),
            entity_type=payload.get(
                "entity_type",
                "generic",
            ),
            properties=payload.get(
                "properties",
                {},
            ),
        )

        self.runtime.memory.remember(
            key="entity_created",
            value=entity.to_dict(),
            namespace="aletheus.knowledge",
            memory_type="semantic",
            tags=[
                "entity",
                "knowledge",
            ],
        )

        context.add_result(
            "entity",
            entity.to_dict(),
        )

        return context


    def entity_search(self, context):

        payload = context.payload

        context.add_result(
            "entities",
            self.runtime.knowledge.search_entities(
                label=payload.get(
                    "label"
                ),
                entity_type=payload.get(
                    "entity_type"
                ),
            ),
        )

        return context


    def relationship_create(self, context):

        payload = context.payload

        relationship = self.runtime.knowledge.create_relationship(
            source_id=payload.get(
                "source_id",
                "",
            ),
            target_id=payload.get(
                "target_id",
                "",
            ),
            relationship_type=payload.get(
                "relationship_type",
                "related_to",
            ),
            properties=payload.get(
                "properties",
                {},
            ),
        )

        self.runtime.memory.remember(
            key="relationship_created",
            value=relationship.to_dict(),
            namespace="aletheus.knowledge",
            memory_type="semantic",
            tags=[
                "relationship",
                "knowledge",
            ],
        )

        context.add_result(
            "relationship",
            relationship.to_dict(),
        )

        return context


    def relationship_search(self, context):

        payload = context.payload

        context.add_result(
            "relationships",
            self.runtime.knowledge.search_relationships(
                source_id=payload.get(
                    "source_id"
                ),
                target_id=payload.get(
                    "target_id"
                ),
                relationship_type=payload.get(
                    "relationship_type"
                ),
            ),
        )

        return context


    def graph_export(self, context):

        context.add_result(
            "graph",
            self.runtime.knowledge.graph_export(),
        )

        return context


    def graph_query(self, context):

        context.add_result(
            "graph_query",
            self.runtime.knowledge.graph_query(
                context.payload.get(
                    "entity_id",
                    "",
                )
            ),
        )

        return context


    def graph_stats(self, context):

        knowledge = self.runtime.knowledge

        if hasattr(
            knowledge,
            "stats",
        ):
            result = knowledge.stats()

        elif hasattr(
            knowledge,
            "statistics",
        ):
            result = knowledge.statistics()

        else:
            result = {
                "status": "unknown"
            }

        context.add_result(
            "graph_stats",
            result,
        )

        return context

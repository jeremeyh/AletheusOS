"""
Graph Command Handlers

Genesis 7 Runtime Orchestration

Extracted from runtime/core.py.
"""

from aletheus.runtime.context import RuntimeContext


def entity_create(runtime, context: RuntimeContext):

    payload = context.payload

    entity = runtime.knowledge.create_entity(
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

    runtime.memory.remember(
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


def entity_search(runtime, context: RuntimeContext):

    payload = context.payload

    context.add_result(
        "entities",
        runtime.knowledge.search_entities(
            label=payload.get("label"),
            entity_type=payload.get("entity_type"),
        ),
    )

    return context


def relationship_create(runtime, context: RuntimeContext):

    payload = context.payload

    relationship = runtime.knowledge.create_relationship(
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

    runtime.memory.remember(
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


def relationship_search(runtime, context: RuntimeContext):

    payload = context.payload

    context.add_result(
        "relationships",
        runtime.knowledge.search_relationships(
            source_id=payload.get("source_id"),
            target_id=payload.get("target_id"),
            relationship_type=payload.get("relationship_type"),
        ),
    )

    return context


def graph_export(runtime, context: RuntimeContext):

    context.add_result(
        "graph",
        runtime.knowledge.graph_export(),
    )

    return context


def graph_query(runtime, context: RuntimeContext):

    context.add_result(
        "graph_query",
        runtime.knowledge.graph_query(
            context.payload.get(
                "entity_id",
                "",
            )
        ),
    )

    return context


def graph_stats(runtime, context: RuntimeContext):

    if hasattr(runtime.knowledge, "stats"):
        result = runtime.knowledge.stats()
    elif hasattr(runtime.knowledge, "statistics"):
        result = runtime.knowledge.statistics()
    else:
        result = {
            "status": getattr(
                runtime.knowledge,
                "status",
                "unknown",
            )
        }

    context.add_result(
        "graph_stats",
        result,
    )

    return context

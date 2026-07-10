"""
Knowledge Graph Command Registration

Genesis 6
"""

from aletheus.runtime.domains import KnowledgeGraphDomain


def register_knowledge_graph_commands(runtime):

    domain = KnowledgeGraphDomain(runtime)
    commands = runtime.commands

    commands.register(
        "knowledge.entity.create",
        domain.entity_create,
    )

    commands.register(
        "knowledge.entity.update",
        domain.entity_update,
    )

    commands.register(
        "knowledge.entity.delete",
        domain.entity_delete,
    )

    commands.register(
        "knowledge.relationship.create",
        domain.relationship_create,
    )

    commands.register(
        "knowledge.relationship.delete",
        domain.relationship_delete,
    )

    commands.register(
        "knowledge.search",
        domain.search,
    )

    commands.register(
        "knowledge.graph",
        domain.graph,
    )

    commands.register(
        "knowledge.neighbors",
        domain.neighbors,
    )

    commands.register(
        "knowledge.infer",
        domain.infer,
    )

    commands.register(
        "knowledge.bootstrap.cardhawk",
        domain.bootstrap_cardhawk,
    )

    commands.register(
        "knowledge.statistics",
        domain.statistics,
    )

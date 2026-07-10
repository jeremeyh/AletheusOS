"""
Graph Command Registration

Genesis 7

Uses GraphCommandAdapter boundary.
"""


def register_graph_commands(runtime):

    commands = runtime.commands

    commands.register(
        "entity.create",
        runtime.graph_adapter.entity_create,
    )

    commands.register(
        "entity.search",
        runtime.graph_adapter.entity_search,
    )

    commands.register(
        "relationship.create",
        runtime.graph_adapter.relationship_create,
    )

    commands.register(
        "relationship.search",
        runtime.graph_adapter.relationship_search,
    )

    commands.register(
        "graph.export",
        runtime.graph_adapter.graph_export,
    )

    commands.register(
        "graph.query",
        runtime.graph_adapter.graph_query,
    )

    commands.register(
        "graph.stats",
        runtime.graph_adapter.graph_stats,
    )

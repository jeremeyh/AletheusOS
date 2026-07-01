"""
Graph Command Registration

Version 4.7.2
"""


def register_graph_commands(runtime):

    commands = runtime.commands

    commands.register(
        "entity.create",
        runtime._cmd_entity_create,
    )

    commands.register(
        "entity.search",
        runtime._cmd_entity_search,
    )

    commands.register(
        "relationship.create",
        runtime._cmd_relationship_create,
    )

    commands.register(
        "relationship.search",
        runtime._cmd_relationship_search,
    )

    commands.register(
        "graph.export",
        runtime._cmd_graph_export,
    )

    commands.register(
        "graph.query",
        runtime._cmd_graph_query,
    )

    commands.register(
        "graph.stats",
        runtime._cmd_graph_stats,
    )

"""
Semantic Command Registration

Version 4.7.6
"""


def register_semantic_commands(runtime):

    commands = runtime.commands

    commands.register(
        "semantic.concept.create",
        runtime._cmd_semantic_concept_create,
    )

    commands.register(
        "semantic.concept.search",
        runtime._cmd_semantic_concept_search,
    )

    commands.register(
        "semantic.assert",
        runtime._cmd_semantic_assert,
    )

    commands.register(
        "semantic.query",
        runtime._cmd_semantic_query,
    )

    commands.register(
        "semantic.explain",
        runtime._cmd_semantic_explain,
    )

    commands.register(
        "semantic.bootstrap.cardhawk",
        runtime._cmd_semantic_bootstrap_cardhawk,
    )

    commands.register(
        "semantic.stats",
        runtime._cmd_semantic_stats,
    )

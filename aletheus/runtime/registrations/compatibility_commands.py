"""
Compatibility Command Registration

Genesis 7

Uses CompatibilityCommandAdapter boundary.
"""


def register_compatibility_commands(runtime):

    commands = runtime.commands

    commands.register(
        "compat.list",
        runtime.compatibility_adapter.list,
    )

    commands.register(
        "compat.statistics",
        runtime.compatibility_adapter.statistics,
    )

    commands.register(
        "compat.resolve",
        runtime.compatibility_adapter.resolve,
    )

    commands.register(
        "compat.contract",
        runtime.compatibility_adapter.contract,
    )

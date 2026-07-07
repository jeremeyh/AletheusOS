"""
Federation Command Registration

Genesis 6
"""

def register_federation_commands(runtime):

    commands = runtime.commands

    commands.register(
        "federation.bootstrap",
        runtime._cmd_federation_bootstrap,
    )

    commands.register(
        "federation.join",
        runtime._cmd_federation_join,
    )

    commands.register(
        "federation.leave",
        runtime._cmd_federation_leave,
    )

    commands.register(
        "federation.discover",
        runtime._cmd_federation_discover,
    )

    commands.register(
        "federation.query",
        runtime._cmd_federation_query,
    )

    commands.register(
        "federation.broadcast",
        runtime._cmd_federation_broadcast,
    )

    commands.register(
        "federation.statistics",
        runtime._cmd_federation_statistics,
    )

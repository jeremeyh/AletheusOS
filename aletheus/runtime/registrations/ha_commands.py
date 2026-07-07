"""
High Availability Command Registration

Genesis 6
"""

def register_ha_commands(runtime):

    commands = runtime.commands

    commands.register(
        "ha.bootstrap",
        runtime._cmd_ha_bootstrap,
    )

    commands.register(
        "ha.join",
        runtime._cmd_ha_join,
    )

    commands.register(
        "ha.leave",
        runtime._cmd_ha_leave,
    )

    commands.register(
        "ha.promote",
        runtime._cmd_ha_promote,
    )

    commands.register(
        "ha.demote",
        runtime._cmd_ha_demote,
    )

    commands.register(
        "ha.failover",
        runtime._cmd_ha_failover,
    )

    commands.register(
        "ha.recover",
        runtime._cmd_ha_recover,
    )

    commands.register(
        "ha.replicate",
        runtime._cmd_ha_replicate,
    )

    commands.register(
        "ha.status",
        runtime._cmd_ha_status,
    )

    commands.register(
        "ha.statistics",
        runtime._cmd_ha_statistics,
    )

"""
Plugin Command Registration

Genesis 6
"""

from aletheus.runtime.domains import PluginDomain


def register_plugin_commands(runtime):
    commands = runtime.commands
    domain = PluginDomain(runtime)

    commands.register(
        "plugin.bootstrap",
        domain.bootstrap,
    )

    commands.register(
        "plugin.install",
        domain.install,
    )

    commands.register(
        "plugin.enable",
        domain.enable,
    )

    commands.register(
        "plugin.disable",
        domain.disable,
    )

    commands.register(
        "plugin.update",
        domain.update,
    )

    commands.register(
        "plugin.remove",
        domain.remove,
    )

    commands.register(
        "plugin.list",
        domain.list,
    )

    commands.register(
        "plugin.status",
        domain.status,
    )

    commands.register(
        "plugin.statistics",
        domain.statistics,
    )

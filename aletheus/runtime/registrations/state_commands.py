"""
Persistence State Command Registration

Genesis 6
"""

from aletheus.runtime.domains import PersistenceDomain


def register_state_commands(runtime):
    commands = runtime.commands
    domain = PersistenceDomain(runtime)

    commands.register(
        "state.bootstrap",
        domain.bootstrap,
    )

    commands.register(
        "state.save",
        domain.save,
    )

    commands.register(
        "state.load",
        domain.load,
    )

    commands.register(
        "state.snapshot",
        domain.snapshot,
    )

    commands.register(
        "state.restore",
        domain.restore,
    )

    commands.register(
        "state.export",
        domain.export,
    )

    commands.register(
        "state.import",
        domain.import_state,
    )

    commands.register(
        "state.statistics",
        domain.statistics,
    )

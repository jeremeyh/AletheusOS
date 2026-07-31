"""
Runtime Command Registration

Genesis 7

Uses RuntimeCommandAdapter boundary.
"""


def register_runtime_commands(runtime):

    commands = runtime.commands

    commands.register(
        "runtime.selftest",
        runtime.runtime_adapter.selftest,
    )

    commands.register(
        "runtime.dashboard",
        runtime.runtime_adapter.dashboard,
    )

    commands.register(
        "runtime.snapshot",
        runtime.runtime_adapter.snapshot,
    )

    commands.register(
        "runtime.audit",
        runtime.runtime_adapter.audit,
    )

    commands.register(
        "runtime.docs",
        runtime.runtime_adapter.docs,
    )

    commands.register(
        "runtime.doctor",
        runtime.runtime_adapter.doctor,
    )

    commands.register(
        "runtime.invariants",
        runtime.runtime_adapter.invariants,
    )

    commands.register(
        "runtime.boot.validate",
        runtime.runtime_adapter.boot_validate,
    )

    commands.register(
        "runtime.health",
        runtime.runtime_adapter.health_report,
    )

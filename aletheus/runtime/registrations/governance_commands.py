"""
Runtime Governance Command Registration

Genesis 6
"""


def register_governance_commands(runtime):

    commands = runtime.commands

    commands.register(
        "spa.assess",
        runtime._cmd_spa_assess,
    )

    commands.register(
        "spa.drift",
        runtime._cmd_spa_drift,
    )

    commands.register(
        "architecture.validate",
        runtime._cmd_architecture_validate,
    )

    commands.register(
        "runtime.audit",
        runtime._cmd_runtime_audit,
    )

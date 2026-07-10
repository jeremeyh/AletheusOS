"""
Architecture Governance Commands

Genesis 6
"""


def register_architecture_governance_commands(runtime):

    runtime.commands.register(
        "architecture.governance.check",
        runtime._cmd_architecture_governance_check,
    )

"""
Architecture Validation Commands

Genesis 6
"""


def register_architecture_commands(runtime):

    runtime.commands.register(
        "architecture.validate",
        runtime._cmd_architecture_validate,
    )

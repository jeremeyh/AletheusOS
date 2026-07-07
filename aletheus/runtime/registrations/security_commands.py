"""
Security Command Registration

Genesis 6
"""

def register_security_commands(runtime):

    commands = runtime.commands

    commands.register(
        "security.bootstrap",
        runtime._cmd_security_bootstrap,
    )

    commands.register(
        "security.authenticate",
        runtime._cmd_security_authenticate,
    )

    commands.register(
        "security.authorize",
        runtime._cmd_security_authorize,
    )

    commands.register(
        "security.policy",
        runtime._cmd_security_policy,
    )

    commands.register(
        "security.role.create",
        runtime._cmd_security_role_create,
    )

    commands.register(
        "security.role.assign",
        runtime._cmd_security_role_assign,
    )

    commands.register(
        "security.audit",
        runtime._cmd_security_audit,
    )

    commands.register(
        "security.statistics",
        runtime._cmd_security_statistics,
    )

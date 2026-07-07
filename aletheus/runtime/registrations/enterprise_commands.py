"""
Enterprise Command Registration

Genesis 6
"""

def register_enterprise_commands(runtime):

    commands = runtime.commands

    commands.register(
        "enterprise.bootstrap.cardhawk",
        runtime._cmd_enterprise_bootstrap_cardhawk,
    )

    commands.register(
        "enterprise.create",
        runtime._cmd_enterprise_create,
    )

    commands.register(
        "enterprise.list",
        runtime._cmd_enterprise_list,
    )

    commands.register(
        "enterprise.stats",
        runtime._cmd_enterprise_stats,
    )

    commands.register(
        "department.create",
        runtime._cmd_department_create,
    )

    commands.register(
        "team.create",
        runtime._cmd_team_create,
    )

    commands.register(
        "policy.create",
        runtime._cmd_policy_create,
    )

    commands.register(
        "governance.check",
        runtime._cmd_governance_check,
    )

    commands.register(
        "audit.history",
        runtime._cmd_audit_history,
    )

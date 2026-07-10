"""
Enterprise Command Registration

Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import EnterpriseDomain


def register_enterprise_commands(runtime):

    domain = EnterpriseDomain(runtime)
    commands = runtime.commands

    commands.register(
        "enterprise.bootstrap.cardhawk",
        domain.bootstrap_cardhawk,
    )

    commands.register(
        "enterprise.create",
        domain.create,
    )

    commands.register(
        "enterprise.list",
        domain.list,
    )

    commands.register(
        "enterprise.stats",
        domain.stats,
    )

    commands.register(
        "department.create",
        domain.department_create,
    )

    commands.register(
        "team.create",
        domain.team_create,
    )

    commands.register(
        "policy.create",
        domain.policy_create,
    )

    commands.register(
        "governance.check",
        domain.governance_check,
    )

    commands.register(
        "audit.history",
        domain.audit_history,
    )

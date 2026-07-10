"""
Security Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import SecurityDomain


def register_security_commands(runtime):
    domain = SecurityDomain(runtime)
    commands = runtime.commands

    commands.register("security.bootstrap", domain.bootstrap)
    commands.register("security.authenticate", domain.authenticate)
    commands.register("security.authorize", domain.authorize)
    commands.register("security.policy", domain.policy)
    commands.register("security.role_create", domain.role_create)
    commands.register("security.role_assign", domain.role_assign)
    commands.register("security.audit", domain.audit)
    commands.register("security.statistics", domain.statistics)

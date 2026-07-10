"""
Tenancy Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import TenancyDomain


def register_tenancy_commands(runtime):
    domain = TenancyDomain(runtime)
    commands = runtime.commands

    commands.register("tenant.bootstrap", domain.bootstrap)
    commands.register("tenant.create", domain.create)
    commands.register("tenant.delete", domain.delete)
    commands.register("tenant.list", domain.list)
    commands.register("tenant.select", domain.select)

    commands.register("workspace.create", domain.workspace_create)
    commands.register("workspace.delete", domain.workspace_delete)
    commands.register("workspace.list", domain.workspace_list)

    commands.register("organization.create", domain.organization_create)
    commands.register("organization.update", domain.organization_update)

    commands.register("tenant.statistics", domain.statistics)
    commands.register("tenant.health", domain.health)

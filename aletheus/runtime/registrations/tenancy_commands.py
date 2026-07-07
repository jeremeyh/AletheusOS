"""
Tenancy Command Registration

Genesis 6
"""

def register_tenancy_commands(runtime):

    commands = runtime.commands

    commands.register(
        "tenant.bootstrap",
        runtime._cmd_tenant_bootstrap,
    )

    commands.register(
        "tenant.create",
        runtime._cmd_tenant_create,
    )

    commands.register(
        "tenant.delete",
        runtime._cmd_tenant_delete,
    )

    commands.register(
        "tenant.list",
        runtime._cmd_tenant_list,
    )

    commands.register(
        "tenant.select",
        runtime._cmd_tenant_select,
    )

    commands.register(
        "workspace.create",
        runtime._cmd_workspace_create,
    )

    commands.register(
        "workspace.delete",
        runtime._cmd_workspace_delete,
    )

    commands.register(
        "workspace.list",
        runtime._cmd_workspace_list,
    )

    commands.register(
        "organization.create",
        runtime._cmd_organization_create,
    )

    commands.register(
        "organization.update",
        runtime._cmd_organization_update,
    )

    commands.register(
        "tenant.statistics",
        runtime._cmd_tenant_statistics,
    )

    commands.register(
        "tenant.health",
        runtime._cmd_tenant_health,
    )

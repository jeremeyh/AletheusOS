"""
Workflow Command Registration

Genesis 6
"""

from aletheus.runtime.domains import WorkflowDomain


def register_workflow_commands(runtime):
    commands = runtime.commands
    domain = WorkflowDomain(runtime)

    commands.register(
        "workflow.bootstrap",
        domain.bootstrap,
    )

    commands.register(
        "workflow.create",
        domain.create,
    )

    commands.register(
        "workflow.start",
        domain.start,
    )

    commands.register(
        "workflow.pause",
        domain.pause,
    )

    commands.register(
        "workflow.resume",
        domain.resume,
    )

    commands.register(
        "workflow.cancel",
        domain.cancel,
    )

    commands.register(
        "workflow.status",
        domain.status,
    )

    commands.register(
        "workflow.statistics",
        domain.statistics,
    )

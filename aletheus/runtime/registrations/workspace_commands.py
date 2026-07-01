"""
Workspace Command Registration

Version 4.7.4
"""


def register_workspace_commands(runtime):

    commands = runtime.commands

    commands.register(
        "workspace.overview",
        runtime._cmd_workspace_overview,
    )

    commands.register(
        "workspace.stats",
        runtime._cmd_workspace_stats,
    )

    commands.register(
        "founder.journal.create",
        runtime._cmd_founder_journal_create,
    )

    commands.register(
        "founder.journal.list",
        runtime._cmd_founder_journal_list,
    )

    commands.register(
        "objective.create",
        runtime._cmd_objective_create,
    )

    commands.register(
        "objective.list",
        runtime._cmd_objective_list,
    )

    commands.register(
        "notification.create",
        runtime._cmd_notification_create,
    )

    commands.register(
        "notification.list",
        runtime._cmd_notification_list,
    )

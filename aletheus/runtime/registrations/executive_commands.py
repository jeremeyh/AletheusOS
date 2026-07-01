"""
Executive Command Registration

Version 4.7.7
"""


def register_executive_commands(runtime):

    commands = runtime.commands

    commands.register(
        "executive.status",
        runtime._cmd_executive_status,
    )

    commands.register(
        "executive.snapshot",
        runtime._cmd_executive_snapshot,
    )

    commands.register(
        "executive.summary",
        runtime._cmd_executive_summary,
    )

    commands.register(
        "executive.recommendations",
        runtime._cmd_executive_recommendations,
    )

    commands.register(
        "executive.risks",
        runtime._cmd_executive_risks,
    )

    commands.register(
        "executive.daily_brief",
        runtime._cmd_executive_daily_brief,
    )

    commands.register(
        "executive.system_report",
        runtime._cmd_executive_system_report,
    )

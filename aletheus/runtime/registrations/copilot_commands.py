"""
Copilot Command Registration

Version 4.8.0
"""


def register_copilot_commands(runtime):

    commands = runtime.commands

    commands.register(
        "copilot.ask",
        runtime._cmd_copilot_ask,
    )

    commands.register(
        "copilot.brief",
        runtime._cmd_copilot_brief,
    )

    commands.register(
        "copilot.recommend",
        runtime._cmd_copilot_recommend,
    )

    commands.register(
        "copilot.timeline",
        runtime._cmd_copilot_timeline,
    )

    commands.register(
        "copilot.history",
        runtime._cmd_copilot_history,
    )

    commands.register(
        "copilot.stats",
        runtime._cmd_copilot_stats,
    )

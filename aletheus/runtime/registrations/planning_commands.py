"""
Planning Command Registration

Version 4.7.9
"""


def register_planning_commands(runtime):

    commands = runtime.commands

    commands.register(
        "planning.create",
        runtime._cmd_planning_create,
    )

    commands.register(
        "planning.list",
        runtime._cmd_planning_list,
    )

    commands.register(
        "planning.execute_next",
        runtime._cmd_planning_execute_next,
    )

    commands.register(
        "planning.execute",
        runtime._cmd_planning_execute,
    )

    commands.register(
        "planning.stats",
        runtime._cmd_planning_stats,
    )

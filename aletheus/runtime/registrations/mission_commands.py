"""
Mission Command Registration

Version 4.7.3
"""


def register_mission_commands(runtime):

    commands = runtime.commands

    commands.register(
        "mission.create",
        runtime._cmd_mission_create,
    )

    commands.register(
        "mission.from_goal",
        runtime._cmd_mission_from_goal,
    )

    commands.register(
        "mission.list",
        runtime._cmd_mission_list,
    )

    commands.register(
        "mission.run",
        runtime._cmd_mission_run,
    )

    commands.register(
        "mission.complete",
        runtime._cmd_mission_complete,
    )

    commands.register(
        "mission.task.complete",
        runtime._cmd_mission_task_complete,
    )

    commands.register(
        "mission.history",
        runtime._cmd_mission_history,
    )

    commands.register(
        "mission.stats",
        runtime._cmd_mission_stats,
    )

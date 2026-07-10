"""
Mission Command Registration

Genesis 7

Uses MissionCommandAdapter boundary.
"""


def register_mission_commands(runtime):

    commands = runtime.commands


    commands.register(
        "mission.create",
        runtime.mission_adapter.create,
    )


    commands.register(
        "mission.from_goal",
        runtime.mission_adapter.from_goal,
    )


    commands.register(
        "mission.list",
        runtime.mission_adapter.list,
    )


    commands.register(
        "mission.run",
        runtime.mission_adapter.run,
    )


    commands.register(
        "mission.complete",
        runtime.mission_adapter.complete,
    )


    commands.register(
        "mission.task.complete",
        runtime.mission_adapter.task_complete,
    )


    commands.register(
        "mission.history",
        runtime.mission_adapter.history,
    )


    commands.register(
        "mission.stats",
        runtime.mission_adapter.stats,
    )

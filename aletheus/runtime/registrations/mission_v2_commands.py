"""
Mission v2 Command Registration

Genesis 6
"""

def register_mission_v2_commands(runtime):

    commands = runtime.commands

    commands.register(
        "mission.v2.create",
        runtime._cmd_mission_v2_create,
    )

    commands.register(
        "mission.v2.plan",
        runtime._cmd_mission_v2_plan,
    )

    commands.register(
        "mission.v2.execute_next",
        runtime._cmd_mission_v2_execute_next,
    )

    commands.register(
        "mission.v2.execute",
        runtime._cmd_mission_v2_execute,
    )

    commands.register(
        "mission.v2.pause",
        runtime._cmd_mission_v2_pause,
    )

    commands.register(
        "mission.v2.resume",
        runtime._cmd_mission_v2_resume,
    )

    commands.register(
        "mission.v2.cancel",
        runtime._cmd_mission_v2_cancel,
    )

    commands.register(
        "mission.v2.list",
        runtime._cmd_mission_v2_list,
    )

    commands.register(
        "mission.v2.telemetry",
        runtime._cmd_mission_v2_telemetry,
    )

    commands.register(
        "mission.v2.stats",
        runtime._cmd_mission_v2_stats,
    )

"""
UIL Command Registration

Version 4.8.1
"""


def register_uil_commands(runtime):

    commands = runtime.commands

    commands.register(
        "uil.context",
        runtime._cmd_uil_context,
    )

    commands.register(
        "uil.reason",
        runtime._cmd_uil_reason,
    )

    commands.register(
        "uil.synthesize",
        runtime._cmd_uil_synthesize,
    )

    commands.register(
        "uil.decide",
        runtime._cmd_uil_decide,
    )

    commands.register(
        "uil.brief",
        runtime._cmd_uil_brief,
    )

    commands.register(
        "uil.snapshot",
        runtime._cmd_uil_snapshot,
    )

    commands.register(
        "uil.timeline",
        runtime._cmd_uil_timeline,
    )

    commands.register(
        "uil.stats",
        runtime._cmd_uil_stats,
    )

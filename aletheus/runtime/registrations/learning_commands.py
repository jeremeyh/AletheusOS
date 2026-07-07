"""
Learning Command Registration

Genesis 6
"""

def register_learning_commands(runtime):

    commands = runtime.commands

    commands.register(
        "learn.record",
        runtime._cmd_learn_record,
    )

    commands.register(
        "learn.lesson",
        runtime._cmd_learn_lesson,
    )

    commands.register(
        "learn.feedback",
        runtime._cmd_learn_feedback,
    )

    commands.register(
        "learn.patterns",
        runtime._cmd_learn_patterns,
    )

    commands.register(
        "learn.improve",
        runtime._cmd_learn_improve,
    )

    commands.register(
        "learn.snapshot",
        runtime._cmd_learn_snapshot,
    )

    commands.register(
        "learn.stats",
        runtime._cmd_learn_stats,
    )

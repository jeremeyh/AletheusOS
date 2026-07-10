"""
Learning Command Registration

Genesis 6
"""

from aletheus.runtime.domains import LearningDomain


def register_learning_commands(runtime):

    commands = runtime.commands
    domain = LearningDomain(runtime)

    commands.register(
        "learning.record",
        domain.record,
    )

    commands.register(
        "learning.lesson",
        domain.lesson,
    )

    commands.register(
        "learning.feedback",
        domain.feedback,
    )

    commands.register(
        "learning.patterns",
        domain.patterns,
    )

    commands.register(
        "learning.improve",
        domain.improve,
    )

    commands.register(
        "learning.snapshot",
        domain.snapshot,
    )

    commands.register(
        "learning.statistics",
        domain.statistics,
    )

"""
Planning Command Registration

Genesis 7 Integration
"""

from __future__ import annotations

from aletheus.runtime.domains import PlanningDomain


def register_planning_commands(runtime):
    """
    Register planning commands.
    """

    domain = PlanningDomain(runtime)

    runtime.commands.register(
        "planning.create",
        domain.create,
    )

    runtime.commands.register(
        "planning.list",
        domain.list,
    )

    runtime.commands.register(
        "planning.execute.next",
        domain.execute_next,
    )

    runtime.commands.register(
        "planning.execute",
        domain.execute,
    )

    runtime.commands.register(
        "planning.statistics",
        domain.statistics,
    )

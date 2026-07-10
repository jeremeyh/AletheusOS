"""
Copilot Command Registration

Genesis 7 Integration
"""

from __future__ import annotations

from aletheus.runtime.domains import CopilotDomain


def register_copilot_commands(runtime):
    """
    Register Copilot commands.
    """

    domain = CopilotDomain(runtime)

    runtime.commands.register(
        "copilot.ask",
        domain.ask,
    )

    runtime.commands.register(
        "copilot.brief",
        domain.brief,
    )

    runtime.commands.register(
        "copilot.recommend",
        domain.recommend,
    )

    runtime.commands.register(
        "copilot.timeline",
        domain.timeline,
    )

    runtime.commands.register(
        "copilot.history",
        domain.history,
    )

    runtime.commands.register(
        "copilot.statistics",
        domain.statistics,
    )

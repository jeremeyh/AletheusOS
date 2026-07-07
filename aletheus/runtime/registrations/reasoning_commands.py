"""
Reasoning Command Registration

Genesis 7 Integration
"""

from __future__ import annotations

from aletheus.runtime.domains import ReasoningDomain


def register_reasoning_commands(runtime):
    """
    Register reasoning command implementations.
    """

    domain = ReasoningDomain(runtime)

    runtime.commands.register(
        "reason.bootstrap",
        domain.bootstrap,
    )

    runtime.commands.register(
        "reason.rule.add",
        domain.rule_add,
    )

    runtime.commands.register(
        "reason.evaluate",
        domain.evaluate,
    )

    runtime.commands.register(
        "reason.explain",
        domain.explain,
    )

    runtime.commands.register(
        "reason.trace",
        domain.trace,
    )

    runtime.commands.register(
        "reason.decision",
        domain.decision,
    )

    runtime.commands.register(
        "reason.confidence",
        domain.confidence,
    )

    runtime.commands.register(
        "reason.statistics",
        domain.statistics,
    )

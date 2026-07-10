"""
Decision Command Registration
Genesis 7 Integration
"""

from __future__ import annotations

from aletheus.runtime.domains import DecisionDomain


def register_decision_commands(runtime):

    domain = DecisionDomain(runtime)

    runtime.commands.register(
        "decision.bootstrap",
        domain.bootstrap,
    )

    runtime.commands.register(
        "decision.policy.add",
        domain.policy_add,
    )

    runtime.commands.register(
        "decision.evaluate",
        domain.evaluate,
    )

    runtime.commands.register(
        "decision.execute",
        domain.execute,
    )

    runtime.commands.register(
        "decision.rollback",
        domain.rollback,
    )

    runtime.commands.register(
        "decision.explain",
        domain.explain,
    )

    runtime.commands.register(
        "decision.history",
        domain.history,
    )

    runtime.commands.register(
        "decision.statistics",
        domain.statistics,
    )

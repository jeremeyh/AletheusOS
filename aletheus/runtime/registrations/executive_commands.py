"""
Executive Command Registration.

Binds executive intelligence commands directly to the bounded
AletheusExecutiveCore.
"""

from __future__ import annotations


def register_executive_commands(runtime):
    commands = runtime.commands
    executive = runtime.executive

    def status(payload=None):
        return executive.stats()

    def snapshot(payload=None):
        return executive.snapshot(runtime)

    def summary(payload=None):
        return executive.summarize(runtime)

    def recommendations(payload=None):
        return executive.generate_recommendations(runtime)

    def risks(payload=None):
        return executive.analyze_risks(runtime)

    def daily_brief(payload=None):
        return executive.daily_brief(runtime)

    def system_report(payload=None):
        return executive.system_report(runtime)

    commands.register(
        "executive.status",
        status,
        replace=True,
    )
    commands.register(
        "executive.snapshot",
        snapshot,
        replace=True,
    )
    commands.register(
        "executive.summary",
        summary,
        replace=True,
    )
    commands.register(
        "executive.recommendations",
        recommendations,
        replace=True,
    )
    commands.register(
        "executive.risks",
        risks,
        replace=True,
    )
    commands.register(
        "executive.daily_brief",
        daily_brief,
        replace=True,
    )
    commands.register(
        "executive.system_report",
        system_report,
        replace=True,
    )

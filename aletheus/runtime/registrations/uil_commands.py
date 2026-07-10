"""
Universal Intelligence Layer Command Registration.

Mounts the bounded UIL composition adapter and exposes its command surface.
"""

from __future__ import annotations



def register_uil_commands(runtime):
    commands = runtime.commands

    uil = runtime.uil

    def context(payload=None):
        payload = payload or {}

        return uil.context(
            question=payload.get("question", ""),
            supplied_context=payload.get("context"),
        )

    def reason(payload=None):
        payload = payload or {}

        return uil.reason(
            question=payload.get("question", ""),
            supplied_context=payload.get("context"),
        )

    def synthesize(payload=None):
        payload = payload or {}

        return uil.synthesize(
            question=payload.get("question", ""),
            supplied_context=payload.get("context"),
        )

    def decide(payload=None):
        payload = payload or {}

        return uil.decide(
            question=payload.get("question", ""),
            supplied_context=payload.get("context"),
        )

    def brief(payload=None):
        return uil.brief()

    def snapshot(payload=None):
        return uil.snapshot()

    def timeline(payload=None):
        payload = payload or {}

        return uil.timeline(
            limit=payload.get("limit", 50),
        )

    def statistics(payload=None):
        return uil.stats()

    commands.register(
        "uil.context",
        context,
        replace=True,
    )
    commands.register(
        "uil.reason",
        reason,
        replace=True,
    )
    commands.register(
        "uil.synthesize",
        synthesize,
        replace=True,
    )
    commands.register(
        "uil.decide",
        decide,
        replace=True,
    )
    commands.register(
        "uil.brief",
        brief,
        replace=True,
    )
    commands.register(
        "uil.snapshot",
        snapshot,
        replace=True,
    )
    commands.register(
        "uil.timeline",
        timeline,
        replace=True,
    )
    commands.register(
        "uil.stats",
        statistics,
        replace=True,
    )

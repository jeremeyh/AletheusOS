"""
Health Manager

Genesis 11.2

Owns runtime health projection.

Health represents operational wellness.

Lifecycle represents runtime execution state.

These are intentionally independent concepts.
"""

from __future__ import annotations

from aletheus.runtime.lifecycle.resolver import (
    resolve_runtime_lifecycle,
)


class HealthManager:
    """
    Canonical runtime health projection.

    Health answers:
        Is the runtime healthy?

    Lifecycle answers:
        What phase is the runtime currently in?
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def health(self) -> dict:

        return {
            "health": "healthy",
            "lifecycle": resolve_runtime_lifecycle(self.runtime),
            "booted": getattr(self.runtime, "booted", True),
            "version": getattr(self.runtime, "version", "unknown"),
            "commands": (
                len(getattr(self.runtime.commands, "commands", {}))
                if hasattr(self.runtime, "commands")
                else 0
            ),
        }

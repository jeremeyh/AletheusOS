from __future__ import annotations

from typing import Any


class IntelligenceDispatcher:
    VERSION = "4.0.0"

    def dispatch(self, runtime: Any, command: str, payload: dict | None = None):
        return runtime.commands.dispatch(command, payload or {})

    def statistics(self):
        return {
            "version": self.VERSION,
            "health": "healthy",
        }


intelligence_dispatcher = IntelligenceDispatcher()

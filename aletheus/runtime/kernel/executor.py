from __future__ import annotations

from typing import Dict, Any


class KernelExecutor:
    VERSION = "4.0.0"

    def __init__(self, runtime):
        self.runtime = runtime

    @property
    def version(self):
        return self.VERSION

    def execute(
        self,
        command: str,
        payload: Dict[str, Any] | None = None,
        priority: int = 5,
    ):
        return self.runtime.intelligence_orchestrator.execute(
            command=command,
            payload=payload or {},
            runtime=self.runtime,
            priority=priority,
        )

    def statistics(self):
        return {
            "version": self.VERSION,
            "health": "healthy",
        }

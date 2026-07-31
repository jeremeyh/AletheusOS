from __future__ import annotations

from typing import Any

from .models import Cortex


class CortexRegistry:
    VERSION = "0.1.0"

    def __init__(self):
        self._cortices: dict[str, Cortex] = {}

    def register(
        self,
        id: str,
        name: str,
        role: str,
        status: str = "inactive",
        metadata: dict[str, Any] | None = None,
    ):
        cortex = Cortex(
            id=id, name=name, role=role, status=status, metadata=metadata or {}
        )
        self._cortices[id] = cortex
        return cortex

    def list(self):
        return list(self._cortices.values())

    def count(self):
        return len(self._cortices)

    def health(self):
        return {
            "name": "Cortex Registry",
            "version": self.VERSION,
            "status": "online",
            "cortices": self.count(),
        }

"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Memory Registry
"""

from __future__ import annotations

from .models import (
    MemoryLifecycle,
    MemoryObject,
    MemoryType,
)


class DoubleHedronRegistry:
    """
    Canonical registry for all Memory Objects.

    This registry preserves governed memories
    while remaining independent from retrieval
    and consolidation logic.
    """

    GENESIS = "48.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._memories: dict[str, MemoryObject] = {}

    def register(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        self._memories[memory.memory_id] = memory

        return memory

    def get(
        self,
        memory_id: str,
    ) -> MemoryObject | None:

        return self._memories.get(memory_id)

    def exists(
        self,
        memory_id: str,
    ) -> bool:

        return memory_id in self._memories

    def all(self) -> list[MemoryObject]:

        return sorted(
            self._memories.values(),
            key=lambda memory: memory.created_at,
        )

    def by_identity(
        self,
        identity: str,
    ) -> list[MemoryObject]:

        return [
            memory for memory in self._memories.values() if memory.identity == identity
        ]

    def by_session(
        self,
        session: str,
    ) -> list[MemoryObject]:

        return [
            memory for memory in self._memories.values() if memory.session == session
        ]

    def by_execution(
        self,
        execution: str,
    ) -> list[MemoryObject]:

        return [
            memory
            for memory in self._memories.values()
            if memory.execution == execution
        ]

    def by_type(
        self,
        memory_type: MemoryType,
    ) -> list[MemoryObject]:

        return [
            memory
            for memory in self._memories.values()
            if memory.memory_type == memory_type
        ]

    def by_lifecycle(
        self,
        lifecycle: MemoryLifecycle,
    ) -> list[MemoryObject]:

        return [
            memory
            for memory in self._memories.values()
            if memory.lifecycle == lifecycle
        ]

    def health(self) -> dict:

        return {
            "name": "Double Hedron Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registered_memories": len(self._memories),
        }

    def statistics(self) -> dict:

        memory_types: dict[str, int] = {}
        lifecycles: dict[str, int] = {}

        for memory in self._memories.values():
            mt = memory.memory_type.value
            lc = memory.lifecycle.value

            memory_types.setdefault(mt, 0)
            lifecycles.setdefault(lc, 0)

            memory_types[mt] += 1
            lifecycles[lc] += 1

        return {
            "name": "Double Hedron Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "registered_memories": len(self._memories),
            "memory_types": memory_types,
            "lifecycles": lifecycles,
        }


double_hedron_registry = DoubleHedronRegistry()

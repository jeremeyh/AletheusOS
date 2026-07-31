"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Memory Retrieval
"""

from __future__ import annotations

from .models import MemoryObject, MemoryType
from .registry import double_hedron_registry


class DoubleHedronRetrieval:
    """
    Retrieves relevant Memory Objects.

    Retrieval does not decide truth.
    Retrieval provides context for future reasoning.
    """

    GENESIS = "48.0"
    VERSION = "1.0.0"

    def recall_by_identity(
        self,
        identity: str,
    ) -> list[MemoryObject]:

        return double_hedron_registry.by_identity(identity)

    def recall_by_session(
        self,
        session: str,
    ) -> list[MemoryObject]:

        return double_hedron_registry.by_session(session)

    def recall_by_execution(
        self,
        execution: str,
    ) -> list[MemoryObject]:

        return double_hedron_registry.by_execution(execution)

    def recall_by_type(
        self,
        memory_type: MemoryType,
    ) -> list[MemoryObject]:

        return double_hedron_registry.by_type(memory_type)

    def recall_relevant(
        self,
        *,
        identity: str | None = None,
        session: str | None = None,
        execution: str | None = None,
        memory_type: MemoryType | None = None,
        limit: int = 10,
    ) -> list[MemoryObject]:

        memories = double_hedron_registry.all()

        if identity:
            memories = [memory for memory in memories if memory.identity == identity]

        if session:
            memories = [memory for memory in memories if memory.session == session]

        if execution:
            memories = [memory for memory in memories if memory.execution == execution]

        if memory_type:
            memories = [
                memory for memory in memories if memory.memory_type == memory_type
            ]

        return memories[:limit]

    def health(self) -> dict:

        return {
            "name": "Double Hedron Retrieval",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


double_hedron_retrieval = DoubleHedronRetrieval()

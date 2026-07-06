"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Core Services
"""

from __future__ import annotations

from .consolidation import (
    double_hedron_consolidation,
)
from .models import (
    MemoryLifecycle,
    MemoryObject,
    MemoryType,
    new_memory_id,
)
from .registry import (
    double_hedron_registry,
)
from .retrieval import (
    double_hedron_retrieval,
)


class DoubleHedron:
    """
    Constitutional Memory Service.

    The Double Hedron is the Foundation's
    active memory participant.

    It receives observations,
    preserves experience,
    recalls relevant context,
    and governs memory maturation.
    """

    GENESIS = "48.0"
    VERSION = "1.0.0"

    def remember(
        self,
        *,
        identity: str,
        capability: str,
        execution: str,
        session: str,
        memory_type: MemoryType,
        observation: str,
        evidence: list[str] | None = None,
        reasoning: list[str] | None = None,
        confidence: float = 0.0,
        provenance: dict | None = None,
        metadata: dict | None = None,
    ) -> MemoryObject:

        memory = MemoryObject(
            memory_id=new_memory_id(),
            identity=identity,
            capability=capability,
            execution=execution,
            session=session,
            memory_type=memory_type,
            lifecycle=MemoryLifecycle.CREATED,
            observation=observation,
            evidence=evidence or [],
            reasoning=reasoning or [],
            confidence=confidence,
            provenance=provenance or {},
            metadata=metadata or {},
        )

        double_hedron_registry.register(memory)

        return memory

    def recall(
        self,
        **kwargs,
    ) -> list[MemoryObject]:

        return double_hedron_retrieval.recall_relevant(**kwargs)

    def consolidate(
        self,
        memory: MemoryObject,
        lifecycle: MemoryLifecycle,
    ) -> MemoryObject:

        return double_hedron_consolidation.promote(
            memory,
            lifecycle,
        )

    def health(self) -> dict:

        return {
            "name": "Double Hedron Session Memory",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": double_hedron_registry.health(),
            "retrieval": double_hedron_retrieval.health(),
            "consolidation": double_hedron_consolidation.health(),
        }

    def statistics(self) -> dict:

        return double_hedron_registry.statistics()


double_hedron = DoubleHedron()
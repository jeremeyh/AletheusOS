"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Memory Consolidation
"""

from __future__ import annotations

from .models import (
    MemoryLifecycle,
    MemoryObject,
)
from .registry import (
    double_hedron_registry,
)


class DoubleHedronConsolidation:
    """
    Governs memory promotion.

    Consolidation determines whether
    a memory should mature through its
    constitutional lifecycle.

    Consolidation does not determine truth.
    It determines whether a memory has earned
    continued participation in cognition.
    """

    GENESIS = "48.0"
    VERSION = "1.0.0"

    def promote(
        self,
        memory: MemoryObject,
        lifecycle: MemoryLifecycle,
    ) -> MemoryObject:

        memory.promote(lifecycle)

        return memory

    def promote_to_observed(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        return self.promote(
            memory,
            MemoryLifecycle.OBSERVED,
        )

    def promote_to_referenced(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        return self.promote(
            memory,
            MemoryLifecycle.REFERENCED,
        )

    def promote_to_validated(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        return self.promote(
            memory,
            MemoryLifecycle.VALIDATED,
        )

    def promote_to_constitutional(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        return self.promote(
            memory,
            MemoryLifecycle.CONSTITUTIONAL,
        )

    def archive(
        self,
        memory: MemoryObject,
    ) -> MemoryObject:

        return self.promote(
            memory,
            MemoryLifecycle.ARCHIVED,
        )

    def consolidate(
        self,
        memory_id: str,
    ) -> MemoryObject | None:
        """
        Future policy engine.

        Today this simply retrieves the memory.

        Future releases will evaluate:

        • Reference frequency
        • Confidence trend
        • Evidence quality
        • Council decisions
        • Reason quality
        • Constitutional relevance
        • Identity significance
        """

        return double_hedron_registry.get(memory_id)

    def health(self) -> dict:

        return {
            "name": "Double Hedron Consolidation",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


double_hedron_consolidation = DoubleHedronConsolidation()

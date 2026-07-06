"""
AletheusOS
Genesis 48.0

Double Hedron Session Memory™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .registry import double_hedron_registry


def statistics() -> dict:
    """
    Canonical statistics interface.

    Statistics answer:

        "What has occurred?"

    Double Hedron publishes governed
    memory statistics for Foundation
    observability.
    """

    memories = double_hedron_registry.all()

    memory_types = Counter()
    lifecycles = Counter()
    capabilities = Counter()
    identities = Counter()

    for memory in memories:

        memory_types[memory.memory_type.value] += 1
        lifecycles[memory.lifecycle.value] += 1
        capabilities[memory.capability] += 1
        identities[memory.identity] += 1

    return {
        "name": "Double Hedron Session Memory",
        "genesis": "48.0",
        "version": "1.0.0",

        "registered_memories": len(memories),

        "memory_types": dict(memory_types),

        "lifecycles": dict(lifecycles),

        "capabilities": dict(capabilities),

        "identities": dict(identities),
    }
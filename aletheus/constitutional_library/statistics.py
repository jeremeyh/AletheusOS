"""
AletheusOS
Genesis 51.0

Constitutional Library™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .registry import constitutional_library_registry


def statistics() -> dict:
    """
    Canonical statistics interface.

    Statistics answer:

        "What institutional knowledge exists?"
    """

    knowledge_objects = constitutional_library_registry.all()

    statuses = Counter()
    knowledge_types = Counter()

    for knowledge in knowledge_objects:
        statuses[knowledge.status.value] += 1
        knowledge_types[knowledge.knowledge_type.value] += 1

    return {
        "name": "Constitutional Library",
        "genesis": "51.0",
        "version": "1.0.0",
        "knowledge_objects": len(knowledge_objects),
        "statuses": dict(statuses),
        "knowledge_types": dict(knowledge_types),
    }

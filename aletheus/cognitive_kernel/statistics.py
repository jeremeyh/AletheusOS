"""
AletheusOS
Genesis 46.1

Cognitive Kernel™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .core import cognitive_kernel


def statistics() -> dict:
    """
    Canonical statistics interface for the Cognitive Kernel.

    Statistics answer:
        "What has happened?"

    Health answers:
        "How are we?"

    These are intentionally separate concerns.
    """

    records = cognitive_kernel.records()

    status_counter = Counter()

    application_counter = Counter()

    capability_counter = Counter()

    for record in records:
        status_counter[record["status"]] += 1

        application_counter[record["application"]] += 1

        capability = record["capability_resolution"].get("capability_id")

        if capability:
            capability_counter[capability] += 1

    return {
        "name": "Cognitive Kernel",
        "genesis": "46.1",
        "version": "1.0.0",
        "records": len(records),
        "status_breakdown": dict(status_counter),
        "applications": dict(application_counter),
        "capabilities": dict(capability_counter),
    }

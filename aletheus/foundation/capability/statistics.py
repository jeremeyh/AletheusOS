"""
AletheusOS
Genesis 47.5

Foundation Capability Base™

Statistics Interface
"""

from __future__ import annotations

from .base import FoundationCapability


def statistics(
    capability: FoundationCapability,
) -> dict:
    """
    Canonical Foundation statistics interface.

    Statistics answer:

        "What has happened?"

    Every Foundation capability publishes
    statistics through this common interface.

    Sentinel™, Studio™, dashboards,
    diagnostics, and future analytics
    consume this interface.
    """

    return capability.statistics()

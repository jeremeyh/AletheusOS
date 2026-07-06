"""
AletheusOS
Genesis 47.5

Foundation Capability Base™

Health Interface
"""

from __future__ import annotations

from .base import FoundationCapability


def health(
    capability: FoundationCapability,
) -> dict:
    """
    Canonical Foundation health interface.

    Every Foundation capability exposes the
    same health contract.

    Sentinel™, Studio™, diagnostics,
    enterprise monitoring, and future SDKs
    should consume this interface instead
    of inspecting implementation details.
    """

    return capability.health()

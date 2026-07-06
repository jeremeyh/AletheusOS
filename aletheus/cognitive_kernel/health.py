"""
AletheusOS
Genesis 46.1

Cognitive Kernel™

Health Interface
"""

from __future__ import annotations

from .core import cognitive_kernel


def health() -> dict:
    """
    Canonical health interface for the Cognitive Kernel.

    This module intentionally contains no business logic.
    It exposes the Kernel's health contract for Foundation
    observability, Sentinel™, and enterprise diagnostics.
    """

    return cognitive_kernel.health()

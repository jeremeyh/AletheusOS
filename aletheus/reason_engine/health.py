"""
AletheusOS
Genesis 49.0

Reason Engine™

Health Interface
"""

from __future__ import annotations

from .core import reason_engine


def health() -> dict:
    """
    Canonical health interface.

    Health answers:

        "Can the Foundation safely
        perform constitutional reasoning?"
    """

    return reason_engine.health()

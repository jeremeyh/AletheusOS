"""
AletheusOS
Genesis 49.0

Reason Engine™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .registry import reason_registry


def statistics() -> dict:
    """
    Canonical statistics interface.

    Statistics answer:

        "What reasoning has occurred?"
    """

    reasons = reason_registry.all()

    statuses = Counter()
    confidence = Counter()
    intents = Counter()

    for reason in reasons:
        statuses[reason.status.value] += 1

        confidence[reason.confidence_label.value] += 1

        intents[reason.intent] += 1

    return {
        "name": "Reason Engine",
        "genesis": "49.0",
        "version": "1.0.0",
        "registered_reasons": len(reasons),
        "statuses": dict(statuses),
        "confidence": dict(confidence),
        "intents": dict(intents),
    }

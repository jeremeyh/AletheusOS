"""
AletheusOS
Genesis 47.0

Canonical Identity Framework™

Statistics Interface
"""

from __future__ import annotations

from collections import Counter

from .registry import canonical_identity_registry


def statistics() -> dict:
    """
    Canonical statistics interface.

    Statistics answer:

        "What has occurred?"

    Health answers:

        "Can we continue operating?"
    """

    identities = canonical_identity_registry.all()

    identity_types = Counter()
    trust_levels = Counter()
    statuses = Counter()

    for identity in identities:
        identity_types[identity.identity_type.value] += 1
        trust_levels[identity.trust_level.value] += 1
        statuses[identity.status.value] += 1

    return {
        "name": "Canonical Identity Framework",
        "genesis": "47.0",
        "version": "1.0.0",
        "registered_identities": len(identities),
        "identity_types": dict(identity_types),
        "trust_levels": dict(trust_levels),
        "statuses": dict(statuses),
    }

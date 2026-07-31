"""
AletheusOS
Genesis 47.0

Canonical Identity Framework™

Identity Registry
"""

from __future__ import annotations

from .models import (
    CanonicalIdentity,
)


class CanonicalIdentityRegistry:
    """
    Canonical registry for all Foundation identities.

    Every governed identity is registered here before it
    participates in constitutional execution.
    """

    GENESIS = "47.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._identities: dict[str, CanonicalIdentity] = {}

    def register(
        self,
        identity: CanonicalIdentity,
    ) -> CanonicalIdentity:

        self._identities[identity.identity_id] = identity

        return identity

    def get(
        self,
        identity_id: str,
    ) -> CanonicalIdentity | None:

        return self._identities.get(identity_id)

    def exists(
        self,
        identity_id: str,
    ) -> bool:

        return identity_id in self._identities

    def all(self) -> list[CanonicalIdentity]:

        return sorted(
            self._identities.values(),
            key=lambda identity: identity.canonical_name.lower(),
        )

    def remove(
        self,
        identity_id: str,
    ) -> bool:

        if identity_id not in self._identities:
            return False

        del self._identities[identity_id]

        return True

    def health(self) -> dict:

        return {
            "name": "Canonical Identity Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registered_identities": len(self._identities),
        }

    def statistics(self) -> dict:

        counts: dict[str, int] = {}

        for identity in self._identities.values():
            identity_type = identity.identity_type.value

            counts.setdefault(identity_type, 0)

            counts[identity_type] += 1

        return {
            "name": "Canonical Identity Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "registered_identities": len(self._identities),
            "identity_types": counts,
        }


canonical_identity_registry = CanonicalIdentityRegistry()

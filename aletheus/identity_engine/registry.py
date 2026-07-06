from __future__ import annotations

from .models import Identity


class IdentityRegistry:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def __init__(self):
        self._identities: dict[str, Identity] = {}

    def register(
        self,
        identity: Identity,
    ) -> Identity:

        self._identities[
            identity.identity_id
        ] = identity

        return identity

    def get(
        self,
        identity_id: str,
    ) -> Identity | None:

        return self._identities.get(
            identity_id
        )

    def unregister(
        self,
        identity_id: str,
    ) -> None:

        self._identities.pop(
            identity_id,
            None,
        )

    def identities(self):

        return list(
            self._identities.values()
        )

    def count(self):

        return len(
            self._identities
        )

    def statistics(self):

        return {
            "identities": self.count(),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }

    def health(self):

        return {
            "status": "healthy",
            **self.statistics(),
        }


identity_registry = IdentityRegistry()

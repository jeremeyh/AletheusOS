from __future__ import annotations

from .models import Identity
from .registry import identity_registry


class IdentityResolver:
    GENESIS = "21.7"
    VERSION = "1.0.0"

    def resolve(
        self,
        value: str,
    ) -> Identity | None:

        value = value.lower()

        for identity in identity_registry.identities():
            if identity.identity_id.lower() == value:
                return identity

            if identity.display_name.lower() == value:
                return identity

            for alias in identity.aliases:
                if alias.lower() == value:
                    return identity

        return None

    def exists(
        self,
        value: str,
    ) -> bool:

        return self.resolve(value) is not None

    def statistics(self):

        return {
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "identities": identity_registry.count(),
        }

    def health(self):

        return {
            "status": "healthy",
            **self.statistics(),
        }


identity_resolver = IdentityResolver()

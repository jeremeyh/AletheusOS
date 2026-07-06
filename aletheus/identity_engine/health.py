from __future__ import annotations

from .authentication import identity_authentication
from .authorization import identity_authorization
from .registry import identity_registry
from .resolver import identity_resolver
from .sessions import session_manager


class IdentityHealth:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def report(self):

        return {
            "subsystem": "Identity Engine",
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "registry": identity_registry.statistics(),
            "resolver": identity_resolver.health(),
            "authentication": identity_authentication.health(),
            "authorization": identity_authorization.health(),
            "sessions": session_manager.statistics(),
        }


identity_health = IdentityHealth()

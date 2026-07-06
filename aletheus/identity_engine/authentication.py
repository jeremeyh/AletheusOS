from __future__ import annotations

from .models import Identity


class IdentityAuthentication:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def authenticate(
        self,
        identity: Identity | None,
    ):

        if identity is None:
            return {
                "authenticated": False,
                "reason": "Identity not found.",
            }

        if identity.status != "active":
            return {
                "authenticated": False,
                "reason": f"Identity is not active: {identity.status}",
            }

        return {
            "authenticated": True,
            "reason": "Identity authenticated.",
            "identity_id": identity.identity_id,
            "profile_id": identity.profile_id,
        }

    def health(self):
        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


identity_authentication = IdentityAuthentication()

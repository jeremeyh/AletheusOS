from __future__ import annotations

from .models import Identity


class IdentityAuthorization:

    GENESIS = "21.7"
    VERSION = "1.0.0"

    def authorize(
        self,
        identity: Identity | None,
        required_profile: str,
    ):

        if identity is None:
            return {
                "authorized": False,
                "reason": "Identity not found.",
            }

        authorized = (
            identity.profile_id == required_profile
        )

        return {
            "authorized": authorized,
            "identity_id": identity.identity_id,
            "required_profile": required_profile,
            "actual_profile": identity.profile_id,
            "reason": (
                "Authorized."
                if authorized
                else "Insufficient profile."
            ),
        }

    def health(self):
        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


identity_authorization = IdentityAuthorization()

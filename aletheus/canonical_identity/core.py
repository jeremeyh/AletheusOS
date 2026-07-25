"""
AletheusOS
Genesis 47.0

Canonical Identity Framework™

Core Services
"""

from __future__ import annotations

from .models import (
    CanonicalIdentity,
    IdentityStatus,
    IdentityType,
    TrustLevel,
    new_identity_id,
)
from .registry import canonical_identity_registry


class CanonicalIdentityFramework:
    """
    Constitutional Identity Service.

    Responsible for creating, registering,
    retrieving and managing canonical identities.

    This is the public API consumed by the
    Cognitive Kernel and future Foundation
    capabilities.
    """

    GENESIS = "47.0"
    VERSION = "1.0.0"

    def create_identity(
        self,
        *,
        canonical_name: str,
        display_name: str,
        identity_type: IdentityType,
        trust_level: TrustLevel,
        organizations: list[str] | None = None,
        roles: list[str] | None = None,
        applications: list[str] | None = None,
        permissions: list[str] | None = None,
        metadata: dict | None = None,
    ) -> CanonicalIdentity:

        identity = CanonicalIdentity(
            identity_id=new_identity_id(),
            canonical_name=canonical_name,
            display_name=display_name,
            identity_type=identity_type,
            trust_level=trust_level,
            status=IdentityStatus.ACTIVE,
            organizations=organizations or [],
            roles=roles or [],
            applications=applications or [],
            permissions=permissions or [],
            metadata=metadata or {},
        )

        canonical_identity_registry.register(identity)

        return identity

    def get_identity(
        self,
        identity_id: str,
    ) -> CanonicalIdentity | None:

        return canonical_identity_registry.get(identity_id)

    def identity_exists(
        self,
        identity_id: str,
    ) -> bool:

        return canonical_identity_registry.exists(identity_id)

    def identities(
        self,
    ) -> list[CanonicalIdentity]:

        return canonical_identity_registry.all()

    def health(self) -> dict:

        return {
            "name": "Canonical Identity Framework",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": canonical_identity_registry.health(),
        }

    def statistics(self) -> dict:

        return canonical_identity_registry.statistics()


canonical_identity_framework = CanonicalIdentityFramework()

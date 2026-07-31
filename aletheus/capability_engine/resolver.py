from __future__ import annotations

from .grants import grant_manager
from .profiles import foundation_profiles


class CapabilityResolver:
    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self._profile_assignments: dict[str, str] = {}

    def assign_profile(
        self,
        identity_id: str,
        profile_id: str,
    ):
        self._profile_assignments[identity_id] = profile_id

    def profile(self, identity_id: str):
        return self._profile_assignments.get(
            identity_id,
            "consumer",
        )

    def resolve_profiles(
        self,
        profile_id: str,
    ):

        resolved = []

        def walk(pid):

            if pid in resolved:
                return

            profile = foundation_profiles.get(pid)

            if not profile:
                return

            resolved.append(pid)

            for parent in profile.inherits:
                walk(parent)

        walk(profile_id)

        return resolved

    def effective_capabilities(
        self,
        identity_id: str,
    ):

        capabilities = set()

        profile = self.profile(identity_id)

        for pid in self.resolve_profiles(profile):
            p = foundation_profiles.get(pid)

            if p:
                capabilities.update(p.capabilities)

        for grant in grant_manager.grants_for(identity_id):
            capabilities.add(grant.capability_id)

        return sorted(capabilities)

    def has(
        self,
        identity_id: str,
        capability_id: str,
    ):

        return capability_id in self.effective_capabilities(identity_id)

    def health(self):

        return {
            "status": "healthy",
            "profiles": len(self._profile_assignments),
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


capability_resolver = CapabilityResolver()

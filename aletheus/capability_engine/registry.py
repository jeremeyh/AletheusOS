from __future__ import annotations

from .models import Capability, CapabilityBundle, CapabilityProfile


class CapabilityRegistry:
    GENESIS = "21.6"
    VERSION = "0.1.0"

    def __init__(self):
        self._capabilities: dict[str, Capability] = {}
        self._profiles: dict[str, CapabilityProfile] = {}
        self._bundles: dict[str, CapabilityBundle] = {}

    def register_capability(self, capability: Capability):
        self._capabilities[capability.capability_id] = capability
        return capability

    def register_profile(self, profile: CapabilityProfile):
        self._profiles[profile.profile_id] = profile
        return profile

    def register_bundle(self, bundle: CapabilityBundle):
        self._bundles[bundle.bundle_id] = bundle
        return bundle

    def capability(self, capability_id: str):
        return self._capabilities.get(capability_id)

    def profile(self, profile_id: str):
        return self._profiles.get(profile_id)

    def bundle(self, bundle_id: str):
        return self._bundles.get(bundle_id)

    def capabilities(self):
        return [item.to_dict() for item in self._capabilities.values()]

    def profiles(self):
        return [item.to_dict() for item in self._profiles.values()]

    def bundles(self):
        return [item.to_dict() for item in self._bundles.values()]

    def statistics(self):
        return {
            "capabilities": len(self._capabilities),
            "profiles": len(self._profiles),
            "bundles": len(self._bundles),
        }

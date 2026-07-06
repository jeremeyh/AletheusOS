from __future__ import annotations


class CapabilityClient:
    def __init__(self, app):
        self.app = app
        self._capabilities: set[str] = set()

    def grant(self, capability_id: str):
        self._capabilities.add(capability_id)
        return {
            "capability_id": capability_id,
            "granted": True,
        }

    def revoke(self, capability_id: str):
        self._capabilities.discard(capability_id)
        return {
            "capability_id": capability_id,
            "granted": False,
        }

    def has(self, capability_id: str):
        return capability_id in self._capabilities

    def list(self):
        return sorted(self._capabilities)

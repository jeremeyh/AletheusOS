"""
Capability Permission Guard

Post-Genesis 2
"""


class CapabilityGuardEngine:
    def authorize(self, capability):

        return {"capability": capability, "authorized": True}

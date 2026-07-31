"""
Capability Entitlement Engine

Genesis 13.45
"""


class EntitlementEngine:
    def check(self, subscription, capability):

        return capability in (subscription.capabilities)

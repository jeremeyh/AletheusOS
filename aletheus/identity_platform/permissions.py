"""
Capability Permission Engine

Genesis 13.44
"""


class PermissionEngine:
    def check(self, identity, capability):

        return capability in (identity.capabilities)

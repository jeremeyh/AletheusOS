"""
AletheusOS Identity Platform Engine

Genesis 13.44
"""

from .organizations import OrganizationRegistry
from .permissions import PermissionEngine
from .policies import PolicyEngine
from .tenants import TenantManager
from .users import UserRegistry


class IdentityPlatformEngine:
    def __init__(self):

        self.users = UserRegistry()

        self.organizations = OrganizationRegistry()

        self.tenants = TenantManager()

        self.permissions = PermissionEngine()

        self.policies = PolicyEngine()

    def authorize(self, identity, capability):

        return self.permissions.check(identity, capability)

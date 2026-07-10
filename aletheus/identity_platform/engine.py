"""
AletheusOS Identity Platform Engine

Genesis 13.44
"""


from .users import UserRegistry
from .organizations import OrganizationRegistry
from .tenants import TenantManager
from .permissions import PermissionEngine
from .policies import PolicyEngine



class IdentityPlatformEngine:


    def __init__(self):

        self.users = UserRegistry()

        self.organizations = OrganizationRegistry()

        self.tenants = TenantManager()

        self.permissions = PermissionEngine()

        self.policies = PolicyEngine()



    def authorize(
        self,
        identity,
        capability
    ):


        return self.permissions.check(

            identity,

            capability

        )


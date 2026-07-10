"""
Tenant Isolation

Genesis 13.44
"""


class TenantManager:


    def __init__(self):

        self.tenants = {}



    def create(
        self,
        tenant
    ):

        self.tenants[
            tenant.tenant_id
        ] = tenant


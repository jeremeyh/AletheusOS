class TenancyDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.tenancy_v3.bootstrap()

    def create(self, payload):
        return self.runtime.tenancy_v3.create_tenant(
            organization_id=payload.get("organization_id"),
            name=payload.get("name", "Production"),
            environment=payload.get("environment", "production"),
            quotas=payload.get("quotas", {}),
            metadata=payload.get("metadata", {}),
        )

    def delete(self, payload):
        return self.runtime.tenancy_v3.delete_tenant(
            payload.get("tenant_id", "")
        )

    def list(self, payload=None):
        return self.runtime.tenancy_v3.list_tenants()

    def select(self, payload):
        return self.runtime.tenancy_v3.select_tenant(
            payload.get("tenant_id", "")
        )

    def workspace_create(self, payload):
        return self.runtime.tenancy_v3.create_workspace(
            tenant_id=payload.get("tenant_id"),
            name=payload.get("name", "Workspace"),
            metadata=payload.get("metadata", {}),
        )

    def workspace_delete(self, payload):
        return self.runtime.tenancy_v3.delete_workspace(
            payload.get("workspace_id", "")
        )

    def workspace_list(self, payload):
        return self.runtime.tenancy_v3.list_workspaces(
            payload.get("tenant_id")
        )

    def organization_create(self, payload):
        return self.runtime.tenancy_v3.create_organization(
            name=payload.get("name", "Organization"),
            metadata=payload.get("metadata", {}),
        )

    def organization_update(self, payload):
        return self.runtime.tenancy_v3.update_organization(
            organization_id=payload.get("organization_id"),
            name=payload.get("name"),
            metadata=payload.get("metadata"),
            status=payload.get("status"),
        )

    def statistics(self, payload=None):
        return self.runtime.tenancy_v3.statistics()

    def health(self, payload=None):
        return self.runtime.tenancy_v3.health()

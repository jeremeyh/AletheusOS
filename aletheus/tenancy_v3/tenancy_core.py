from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now():
    return utc_now_iso()


@dataclass
class Organization:
    organization_id: str
    name: str
    status: str = "active"
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Tenant:
    tenant_id: str
    organization_id: str
    name: str
    environment: str = "production"
    status: str = "active"
    created_at: str = field(default_factory=utc_now)
    quotas: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Workspace:
    workspace_id: str
    tenant_id: str
    name: str
    status: str = "active"
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


class AletheusTenancyEngine:
    VERSION = "3.9.0"

    def __init__(self):
        self.organizations: dict[str, Organization] = {}
        self.tenants: dict[str, Tenant] = {}
        self.workspaces: dict[str, Workspace] = {}
        self.active_tenant_id: str | None = None

    @property
    def version(self):
        return self.VERSION

    def bootstrap(self):
        if not self.organizations:
            org = self.create_organization(
                name="Card Hawk",
                metadata={
                    "purpose": "First production tenant for AletheusOS",
                    "owner": "6th Dimension Multimedia",
                },
            )

            tenant = self.create_tenant(
                organization_id=org["organization_id"],
                name="Production",
                environment="production",
                quotas={
                    "agents": 25,
                    "workflows": 100,
                    "plugins": 50,
                    "storage_mb": 1024,
                },
            )

            self.create_workspace(
                tenant_id=tenant["tenant_id"],
                name="Founder Workspace",
            )

            self.create_workspace(
                tenant_id=tenant["tenant_id"],
                name="Card Hawk Engineering",
            )

            self.active_tenant_id = tenant["tenant_id"]

        return self.statistics()

    def create_organization(self, name: str, metadata=None):
        organization = Organization(
            organization_id=str(uuid.uuid4()),
            name=name,
            metadata=metadata or {},
        )

        self.organizations[organization.organization_id] = organization

        return asdict(organization)

    def update_organization(self, organization_id: str, name=None, metadata=None, status=None):
        organization = self.organizations.get(organization_id)

        if organization is None:
            return {"error": "Organization not found"}

        if name is not None:
            organization.name = name

        if metadata is not None:
            organization.metadata.update(metadata)

        if status is not None:
            organization.status = status

        return asdict(organization)

    def create_tenant(
        self,
        organization_id: str,
        name: str,
        environment: str = "production",
        quotas=None,
        metadata=None,
    ):
        if organization_id not in self.organizations:
            return {"error": "Organization not found"}

        tenant = Tenant(
            tenant_id=str(uuid.uuid4()),
            organization_id=organization_id,
            name=name,
            environment=environment,
            quotas=quotas or {},
            metadata=metadata or {},
        )

        self.tenants[tenant.tenant_id] = tenant

        if self.active_tenant_id is None:
            self.active_tenant_id = tenant.tenant_id

        return asdict(tenant)

    def delete_tenant(self, tenant_id: str):
        tenant = self.tenants.pop(tenant_id, None)

        if tenant is None:
            return {"error": "Tenant not found"}

        self.workspaces = {
            workspace_id: workspace
            for workspace_id, workspace in self.workspaces.items()
            if workspace.tenant_id != tenant_id
        }

        if self.active_tenant_id == tenant_id:
            self.active_tenant_id = next(iter(self.tenants.keys()), None)

        return asdict(tenant)

    def list_tenants(self):
        return {
            "active_tenant_id": self.active_tenant_id,
            "tenants": [asdict(t) for t in self.tenants.values()],
        }

    def select_tenant(self, tenant_id: str):
        if tenant_id not in self.tenants:
            return {"error": "Tenant not found"}

        self.active_tenant_id = tenant_id

        return {
            "selected": True,
            "tenant": asdict(self.tenants[tenant_id]),
        }

    def create_workspace(self, tenant_id: str, name: str, metadata=None):
        if tenant_id not in self.tenants:
            return {"error": "Tenant not found"}

        workspace = Workspace(
            workspace_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            name=name,
            metadata=metadata or {},
        )

        self.workspaces[workspace.workspace_id] = workspace

        return asdict(workspace)

    def delete_workspace(self, workspace_id: str):
        workspace = self.workspaces.pop(workspace_id, None)

        if workspace is None:
            return {"error": "Workspace not found"}

        return asdict(workspace)

    def list_workspaces(self, tenant_id=None):
        workspaces = list(self.workspaces.values())

        if tenant_id:
            workspaces = [
                workspace
                for workspace in workspaces
                if workspace.tenant_id == tenant_id
            ]

        return {
            "workspaces": [asdict(w) for w in workspaces],
        }

    def health(self):
        return {
            "health": "healthy",
            "organizations": len(self.organizations),
            "tenants": len(self.tenants),
            "workspaces": len(self.workspaces),
            "active_tenant_id": self.active_tenant_id,
        }

    def statistics(self):
        return {
            "version": self.VERSION,
            "organizations": len(self.organizations),
            "tenants": len(self.tenants),
            "workspaces": len(self.workspaces),
            "active_tenant_id": self.active_tenant_id,
            "health": "healthy",
        }


tenancy_core = AletheusTenancyEngine()

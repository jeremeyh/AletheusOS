from __future__ import annotations

from typing import Any

from aletheus.enterprise.models import (
    AuditRecord,
    EnterpriseDepartment,
    EnterpriseOrganization,
    EnterprisePolicy,
    EnterpriseTeam,
)


class AletheusEnterpriseCore:
    def __init__(self) -> None:
        self.version = "2.1.0"
        self.organizations: list[EnterpriseOrganization] = []
        self.audit_records: list[AuditRecord] = []

    def audit(
        self,
        actor: str,
        action: str,
        target: str,
        outcome: str = "recorded",
        metadata: dict[str, Any] | None = None,
    ) -> AuditRecord:
        record = AuditRecord(
            actor=actor,
            action=action,
            target=target,
            outcome=outcome,
            metadata=metadata or {},
        )
        self.audit_records.append(record)
        return record

    def create_organization(
        self,
        name: str,
        description: str = "",
        applications: list[str] | None = None,
    ) -> EnterpriseOrganization:
        existing = self.get_organization(name=name)
        if existing:
            return existing

        org = EnterpriseOrganization(
            name=name,
            description=description,
            applications=applications or [],
        )
        self.organizations.append(org)
        self.audit("system", "organization.created", org.name, "success", org.to_dict())
        return org

    def bootstrap_cardhawk_enterprise(self) -> EnterpriseOrganization:
        org = self.create_organization(
            name="Card Hawk Enterprise™",
            description="First native enterprise deployed on AletheusOS.",
            applications=[
                "Card Hawk Foundation™",
                "Asset Vault",
                "Portfolio Engine",
                "Marketplace Intelligence",
                "Hawk A•Eye™",
                "THORᵡ",
                "DEF",
                "FALCON™",
                "NEST™",
            ],
        )

        self.create_department(
            organization_id=org.organization_id,
            name="Collectible Intelligence",
            description="Portfolio, marketplace, and asset intelligence operations.",
        )

        self.create_department(
            organization_id=org.organization_id,
            name="Autonomous Operations",
            description="Missions, workflows, agents, and optimization.",
        )

        self.create_policy(
            organization_id=org.organization_id,
            name="Founder Approval Required",
            description="Critical acquisition, deletion, or external execution actions require founder review.",
            scope="enterprise",
            rules=[
                "require_founder_approval_for_purchase_execution",
                "require_founder_approval_for_external_api_actions",
                "log_all_marketplace_decisions",
            ],
        )

        return org

    def get_organization(
        self, organization_id: str = "", name: str = ""
    ) -> EnterpriseOrganization | None:
        for org in self.organizations:
            if organization_id and org.organization_id == organization_id:
                return org
            if name and org.name == name:
                return org
        return None

    def list_organizations(self) -> list[dict[str, Any]]:
        return [org.to_dict() for org in self.organizations]

    def create_department(
        self,
        organization_id: str,
        name: str,
        description: str = "",
    ) -> dict[str, Any]:
        org = self.get_organization(organization_id=organization_id)
        if org is None:
            return {"error": f"Organization not found: {organization_id}"}

        existing = next(
            (department for department in org.departments if department.name == name),
            None,
        )
        if existing:
            return existing.to_dict()

        department = EnterpriseDepartment(name=name, description=description)
        org.departments.append(department)
        self.audit(
            "system", "department.created", name, "success", department.to_dict()
        )
        return department.to_dict()

    def create_team(
        self,
        organization_id: str,
        department_id: str,
        name: str,
        description: str = "",
        members: list[str] | None = None,
    ) -> dict[str, Any]:
        org = self.get_organization(organization_id=organization_id)
        if org is None:
            return {"error": f"Organization not found: {organization_id}"}

        department = next(
            (item for item in org.departments if item.department_id == department_id),
            None,
        )
        if department is None:
            return {"error": f"Department not found: {department_id}"}

        team = EnterpriseTeam(name=name, description=description, members=members or [])
        department.teams.append(team)
        self.audit("system", "team.created", name, "success", team.to_dict())
        return team.to_dict()

    def create_policy(
        self,
        organization_id: str,
        name: str,
        description: str = "",
        scope: str = "enterprise",
        rules: list[str] | None = None,
    ) -> dict[str, Any]:
        org = self.get_organization(organization_id=organization_id)
        if org is None:
            return {"error": f"Organization not found: {organization_id}"}

        existing = next(
            (policy for policy in org.policies if policy.name == name), None
        )
        if existing:
            return existing.to_dict()

        policy = EnterprisePolicy(
            name=name,
            description=description,
            scope=scope,
            rules=rules or [],
        )
        org.policies.append(policy)
        self.audit("system", "policy.created", name, "success", policy.to_dict())
        return policy.to_dict()

    def governed_action(
        self,
        actor: str,
        action: str,
        target: str,
        organization_id: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        org = (
            self.get_organization(organization_id=organization_id)
            if organization_id
            else None
        )

        requires_review = False
        if org:
            for policy in org.policies:
                rules = " ".join(policy.rules).lower()
                if "founder_approval" in rules and any(
                    word in action.lower()
                    for word in ["purchase", "delete", "external", "execute"]
                ):
                    requires_review = True

        outcome = "requires_founder_review" if requires_review else "approved"
        record = self.audit(actor, action, target, outcome, metadata or {})

        return {
            "approved": not requires_review,
            "outcome": outcome,
            "audit": record.to_dict(),
        }

    def audit_history(self) -> list[dict[str, Any]]:
        return [record.to_dict() for record in self.audit_records]

    def stats(self) -> dict[str, Any]:
        departments = sum(len(org.departments) for org in self.organizations)
        teams = sum(
            len(department.teams)
            for org in self.organizations
            for department in org.departments
        )
        policies = sum(len(org.policies) for org in self.organizations)
        applications = sum(len(org.applications) for org in self.organizations)

        return {
            "version": self.version,
            "organizations": len(self.organizations),
            "departments": departments,
            "teams": teams,
            "policies": policies,
            "applications": applications,
            "audit_events": len(self.audit_records),
            "compliance_score": 0.92 if policies else 0.75,
        }


enterprise_core = AletheusEnterpriseCore()

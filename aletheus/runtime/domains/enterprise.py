from __future__ import annotations


class EnterpriseDomain:
    """
    Runtime Enterprise capability domain.
    Genesis 6 migration.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap_cardhawk(self, context):
        result = self.runtime.enterprise.bootstrap_cardhawk_enterprise()
        context.add_result("enterprise", result.to_dict())
        return context

    def create(self, context):
        payload = context.payload

        result = self.runtime.enterprise.create_organization(
            name=payload.get("name", "Untitled Organization"),
            description=payload.get("description", ""),
            applications=payload.get("applications", []),
        )

        context.add_result("enterprise", result.to_dict())
        return context

    def list(self, context):
        context.add_result(
            "enterprises",
            self.runtime.enterprise.list_organizations(),
        )
        return context

    def stats(self, context):
        context.add_result(
            "enterprise_stats",
            self.runtime.enterprise.stats(),
        )
        return context

    def department_create(self, context):
        payload = context.payload

        result = self.runtime.enterprise.create_department(
            organization_id=payload.get("organization_id", ""),
            name=payload.get("name", ""),
            description=payload.get("description", ""),
        )

        context.add_result("department", result)
        return context

    def team_create(self, context):
        payload = context.payload

        result = self.runtime.enterprise.create_team(
            organization_id=payload.get("organization_id", ""),
            department_id=payload.get("department_id", ""),
            name=payload.get("name", ""),
            description=payload.get("description", ""),
            members=payload.get("members", []),
        )

        context.add_result("team", result)
        return context

    def policy_create(self, context):
        payload = context.payload

        result = self.runtime.enterprise.create_policy(
            organization_id=payload.get("organization_id", ""),
            name=payload.get("name", ""),
            description=payload.get("description", ""),
            scope=payload.get("scope", "enterprise"),
            rules=payload.get("rules", []),
        )

        context.add_result("policy", result)
        return context

    def governance_check(self, context):
        payload = context.payload

        result = self.runtime.enterprise.governed_action(
            actor=payload.get("actor", "system"),
            action=payload.get("action", ""),
            target=payload.get("target", ""),
            organization_id=payload.get("organization_id", ""),
            metadata=payload.get("metadata", {}),
        )

        context.add_result("governance", result)
        return context

    def audit_history(self, context):
        history = self.runtime.enterprise.audit_history()

        # Canonical v2.1 result plus historical compatibility alias.
        context.add_result("audit", history)
        context.add_result("audit_history", history)

        return context

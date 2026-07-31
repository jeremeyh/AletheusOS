from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_tenant_bootstrap" in text:
    print("✔ Tenant handlers already exist.")
    raise SystemExit(0)

handlers = """

    # ==========================================================
    # v3.9 Multi-Tenant Runtime
    # ==========================================================

    def _cmd_tenant_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "tenant",
            self.tenancy_v3.bootstrap(),
        )
        return context

    def _cmd_tenant_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "tenant",
            self.tenancy_v3.create_tenant(
                organization_id=payload.get("organization_id"),
                name=payload.get("name", "Production"),
                environment=payload.get("environment", "production"),
                quotas=payload.get("quotas", {}),
                metadata=payload.get("metadata", {}),
            ),
        )
        return context

    def _cmd_tenant_delete(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "tenant",
            self.tenancy_v3.delete_tenant(
                context.payload.get("tenant_id", "")
            ),
        )
        return context

    def _cmd_tenant_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "tenants",
            self.tenancy_v3.list_tenants(),
        )
        return context

    def _cmd_tenant_select(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "selection",
            self.tenancy_v3.select_tenant(
                context.payload.get("tenant_id", "")
            ),
        )
        return context

    # ----------------------------------------------------------

    def _cmd_workspace_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "workspace",
            self.tenancy_v3.create_workspace(
                tenant_id=payload.get("tenant_id"),
                name=payload.get("name", "Workspace"),
                metadata=payload.get("metadata", {}),
            ),
        )
        return context

    def _cmd_workspace_delete(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "workspace",
            self.tenancy_v3.delete_workspace(
                context.payload.get("workspace_id", "")
            ),
        )
        return context

    def _cmd_workspace_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "workspaces",
            self.tenancy_v3.list_workspaces(
                context.payload.get("tenant_id")
            ),
        )
        return context

    # ----------------------------------------------------------

    def _cmd_organization_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "organization",
            self.tenancy_v3.create_organization(
                name=payload.get("name", "Organization"),
                metadata=payload.get("metadata", {}),
            ),
        )
        return context

    def _cmd_organization_update(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        context.add_result(
            "organization",
            self.tenancy_v3.update_organization(
                organization_id=payload.get("organization_id"),
                name=payload.get("name"),
                metadata=payload.get("metadata"),
                status=payload.get("status"),
            ),
        )
        return context

    # ----------------------------------------------------------

    def _cmd_tenant_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "tenant_stats",
            self.tenancy_v3.statistics(),
        )
        return context

    def _cmd_tenant_health(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "tenant_health",
            self.tenancy_v3.health(),
        )
        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.9 Multi-Tenant Runtime handlers added.")

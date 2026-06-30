from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "from aletheus.tenancy_v3 import tenancy_core" not in text:
    anchor = "from aletheus.security_v3 import security_core"
    if anchor not in text:
        raise SystemExit("Security import anchor not found.")
    text = text.replace(anchor, anchor + "\nfrom aletheus.tenancy_v3 import tenancy_core", 1)

if "self.tenancy_v3 = tenancy_core" not in text:
    anchor = "self.security_v3 = security_core"
    if anchor not in text:
        raise SystemExit("Security runtime anchor not found.")
    text = text.replace(anchor, anchor + "\n        self.tenancy_v3 = tenancy_core", 1)

text = text.replace('self.version = "3.7.0"', 'self.version = "3.9.0"')
text = text.replace('self.version = "3.8.0"', 'self.version = "3.9.0"')

if 'self.commands.register("tenant.bootstrap"' not in text:
    anchor = 'self.commands.register("security.statistics", self._cmd_security_statistics)'
    if anchor not in text:
        raise SystemExit("Security command anchor not found.")

    text = text.replace(anchor, anchor + '''

        # v3.9 Multi-Tenant Runtime
        self.commands.register("tenant.bootstrap", self._cmd_tenant_bootstrap)
        self.commands.register("tenant.create", self._cmd_tenant_create)
        self.commands.register("tenant.delete", self._cmd_tenant_delete)
        self.commands.register("tenant.list", self._cmd_tenant_list)
        self.commands.register("tenant.select", self._cmd_tenant_select)
        self.commands.register("workspace.create", self._cmd_workspace_create)
        self.commands.register("workspace.delete", self._cmd_workspace_delete)
        self.commands.register("workspace.list", self._cmd_workspace_list)
        self.commands.register("organization.create", self._cmd_organization_create)
        self.commands.register("organization.update", self._cmd_organization_update)
        self.commands.register("tenant.statistics", self._cmd_tenant_statistics)
        self.commands.register("tenant.health", self._cmd_tenant_health)
''', 1)

core.write_text(text)
print("✔ v3.9 tenancy runtime integrated.")

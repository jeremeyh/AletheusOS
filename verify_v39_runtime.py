from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v3.9 Runtime Verification")
print("=" * 60)

print("\nTenancy Runtime:")
print(" present:", hasattr(runtime_core, "tenancy_v3"))

if hasattr(runtime_core, "tenancy_v3"):
    print(" version:", runtime_core.tenancy_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

services = ctx.results["diagnostics"]["services"]

print("\nTenancy Registered:")
print(" ", "Aletheus Multi-Tenant Runtime" in services)

expected = [
    "tenant.bootstrap",
    "tenant.create",
    "tenant.delete",
    "tenant.list",
    "tenant.select",
    "workspace.create",
    "workspace.delete",
    "workspace.list",
    "organization.create",
    "organization.update",
    "tenant.statistics",
    "tenant.health",
]

registered = runtime_core.commands.list()

missing = [c for c in expected if c not in registered]

print("\nMissing Commands:")
print(missing)

print("\nTotal Commands:", len(registered))

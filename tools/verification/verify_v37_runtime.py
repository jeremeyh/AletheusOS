from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v3.7 Runtime Verification")
print("=" * 60)

print("\nSecurity Runtime:")
print("  present:", hasattr(runtime_core, "security_v3"))

if hasattr(runtime_core, "security_v3"):
    print("  version:", runtime_core.security_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

services = ctx.results["diagnostics"]["services"]

print("\nSecurity Registered:")
print(" ", "Aletheus Security & Policy Engine" in services)

expected = [
    "security.bootstrap",
    "security.authenticate",
    "security.authorize",
    "security.policy",
    "security.role.create",
    "security.role.assign",
    "security.audit",
    "security.statistics",
]

missing = [c for c in expected if c not in runtime_core.commands.list()]

print("\nMissing Commands:")
print(missing)

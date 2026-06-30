from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v3.6 Runtime Verification")
print("=" * 60)

print("\nHigh Availability Runtime:")
print("  present:", hasattr(runtime_core, "high_availability_v3"))

if hasattr(runtime_core, "high_availability_v3"):
    print("  version:", runtime_core.high_availability_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

services = ctx.results["diagnostics"]["services"]

print("\nHA Service Registered:")
print(" ", "Aletheus High Availability Platform" in services)

expected = [
    "ha.bootstrap",
    "ha.join",
    "ha.leave",
    "ha.promote",
    "ha.demote",
    "ha.failover",
    "ha.recover",
    "ha.replicate",
    "ha.status",
    "ha.statistics",
]

registered = runtime_core.commands.list()

missing = [c for c in expected if c not in registered]

print("\nMissing Commands:")
print(missing)

print("\nTotal Commands:", len(registered))

print("\nBootstrapping HA...")
ctx = runtime_core.commands.dispatch("ha.bootstrap", {})

print("\nErrors:")
print(ctx.errors)

print("\nResults:")
print(ctx.results)

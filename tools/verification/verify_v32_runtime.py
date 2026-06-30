from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v3.2 Runtime Verification")
print("=" * 60)

print("\nPersistence Runtime:")
print("  present:", hasattr(runtime_core, "persistence_v3"))

if hasattr(runtime_core, "persistence_v3"):
    print("  version:", runtime_core.persistence_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

services = ctx.results["diagnostics"]["services"]

print("\nPersistence Service Registered:")
print(" ", "Aletheus Persistence Engine" in services)

expected = [
    "state.bootstrap",
    "state.save",
    "state.load",
    "state.snapshot",
    "state.restore",
    "state.export",
    "state.import",
    "state.statistics",
]

registered = runtime_core.commands.list()

missing = [c for c in expected if c not in registered]

print("\nMissing Commands:")
print(missing)

print("\nTotal Commands:", len(registered))

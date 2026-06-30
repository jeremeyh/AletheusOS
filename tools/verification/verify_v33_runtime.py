from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v3.3 Runtime Verification")
print("=" * 60)

print("\nEvent Bus Runtime:")
print("  present:", hasattr(runtime_core, "event_bus_v3"))

if hasattr(runtime_core, "event_bus_v3"):
    print("  version:", runtime_core.event_bus_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

services = ctx.results["diagnostics"]["services"]

print("\nEvent Bus Registered:")
print(" ", "Aletheus Event Bus" in services)

expected = [
    "event.bootstrap",
    "event.publish",
    "event.subscribe",
    "event.unsubscribe",
    "event.history",
    "event.replay",
    "event.statistics",
]

registered = runtime_core.commands.list()

missing = [c for c in expected if c not in registered]

print("\nMissing Commands:")
print(missing)

print("\nTotal Commands:", len(registered))

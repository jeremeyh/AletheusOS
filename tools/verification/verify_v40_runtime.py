from aletheus.runtime import runtime_core

print("=" * 60)
print("AletheusOS v4.0 Runtime Verification")
print("=" * 60)

print("\nKernel Components")

print(hasattr(runtime_core, "intelligence_orchestrator"))
print(hasattr(runtime_core, "intelligence_scheduler"))
print(hasattr(runtime_core, "intelligence_dispatcher"))
print(hasattr(runtime_core, "intelligence_supervisor"))

ctx = runtime_core.commands.dispatch("kernel.bootstrap")

print("\nErrors:")
print(ctx.errors)

print("\nResults:")
print(ctx.results)

print("\nRegistered Kernel Commands:")

for c in runtime_core.commands.list():
    if c.startswith("kernel."):
        print("-", c)

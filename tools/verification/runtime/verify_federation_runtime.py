from aletheus.runtime import runtime_core

print("federation_v3:", hasattr(runtime_core, "federation_v3"))

if hasattr(runtime_core, "federation_v3"):
    print("VERSION:", runtime_core.federation_v3.VERSION)

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

print("\nSERVICES")
for service in ctx.results["diagnostics"]["services"]:
    print("-", service)

from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

print("\nSERVICES\n")
for service in ctx.results["diagnostics"]["services"]:
    if "Workflow" in service:
        print(service)

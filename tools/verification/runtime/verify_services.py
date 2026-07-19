from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

print("\nSERVICES")
for s in ctx.results["diagnostics"]["services"]:
    print("-", s)

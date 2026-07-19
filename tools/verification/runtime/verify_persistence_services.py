from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("runtime.diagnostics")

for service in ctx.results["diagnostics"]["services"]:
    print(service)

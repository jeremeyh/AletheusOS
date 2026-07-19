from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("runtime.diagnostics")
print(ctx.results["diagnostics"]["services"])

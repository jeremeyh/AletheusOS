from pprint import pprint
from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("cluster.bootstrap", {})

print("\nERRORS")
pprint(ctx.errors)

print("\nRESULTS")
pprint(ctx.results)

print("\nCLUSTER RESULT")
pprint(ctx.results.get("cluster"))

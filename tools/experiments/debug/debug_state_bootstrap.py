from pprint import pprint

from aletheus.runtime import runtime_core

ctx = runtime_core.commands.dispatch("state.bootstrap", {})

print("=" * 60)
print("ERRORS")
print("=" * 60)
pprint(ctx.errors)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
pprint(ctx.results)

print("\n" + "=" * 60)
print("STATE")
print("=" * 60)
pprint(ctx.results.get("state"))

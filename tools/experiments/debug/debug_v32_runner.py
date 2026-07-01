from pprint import pprint
from aletheus.runtime import runtime_core

tests = [
    ("state.bootstrap", {}),
    ("state.save", {}),
    ("state.load", {}),
    ("state.snapshot", {"name": "Debug Snapshot"}),
    ("state.export", {}),
    ("state.statistics", {}),
]

for command, payload in tests:
    print("\n" + "=" * 80)
    print(command)
    print("=" * 80)

    ctx = runtime_core.commands.dispatch(command, payload)

    print("\nErrors:")
    pprint(ctx.errors)

    print("\nResult Keys:")
    pprint(list(ctx.results.keys()))

    print("\nResults:")
    pprint(ctx.results)

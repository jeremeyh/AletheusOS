from pprint import pprint
from aletheus.runtime import runtime_core

commands = [
    "state.bootstrap",
    "state.save",
    "state.load",
    "state.statistics",
]

for cmd in commands:
    print("\n" + "=" * 80)
    print(cmd)
    print("=" * 80)

    ctx = runtime_core.commands.dispatch(cmd, {})

    print("\nErrors:")
    pprint(ctx.errors)

    print("\nResults:")
    pprint(ctx.results)

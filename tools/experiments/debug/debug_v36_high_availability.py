from pprint import pprint
from aletheus.runtime import runtime_core

commands = [
    ("ha.bootstrap", {}),
    ("ha.join", {"name": "Replica Runtime"}),
    ("ha.status", {}),
    ("ha.replicate", {"payload": {"asset": "Card Hawk"}}),
    ("ha.failover", {}),
    ("ha.statistics", {}),
]

for command, payload in commands:
    print("\n" + "=" * 80)
    print(command)
    print("=" * 80)

    ctx = runtime_core.commands.dispatch(command, payload)

    print("\nErrors:")
    pprint(ctx.errors)

    print("\nResults:")
    pprint(ctx.results)

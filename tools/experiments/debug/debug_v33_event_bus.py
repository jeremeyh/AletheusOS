from pprint import pprint

from aletheus.runtime import runtime_core

tests = [
    ("event.bootstrap", {}),
    (
        "event.publish",
        {
            "topic": "runtime.test",
            "publisher": "debug",
            "payload": {"hello": "world"},
        },
    ),
    (
        "event.subscribe",
        {
            "topic": "runtime.test",
            "subscriber": "Workflow Engine",
        },
    ),
    (
        "event.history",
        {
            "topic": "runtime.test",
        },
    ),
    (
        "event.replay",
        {
            "topic": "runtime.test",
        },
    ),
    ("event.statistics", {}),
]

for command, payload in tests:
    print("\n" + "=" * 80)
    print(command)
    print("=" * 80)

    ctx = runtime_core.commands.dispatch(command, payload)

    print("\nErrors:")
    pprint(ctx.errors)

    print("\nResults:")
    pprint(ctx.results)

#!/bin/bash

set -e

echo "=== Genesis 7 Event Adapter Extraction ==="


mkdir -p aletheus/runtime/adapters


cat > aletheus/runtime/adapters/event_adapter.py <<'PY'
"""
Event Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns EventBus command execution boundary.
"""


class EventCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def bootstrap(self, context):

        context.add_result(
            "event_bus",
            self.runtime.event_bus_v3.bootstrap(),
        )

        return context


    def publish(self, context):

        payload = context.payload

        context.add_result(
            "event",
            self.runtime.event_bus_v3.publish(
                topic=payload.get(
                    "topic",
                    "runtime.event",
                ),
                payload=payload.get(
                    "payload",
                    {},
                ),
                publisher=payload.get(
                    "publisher",
                    "runtime",
                ),
                priority=payload.get(
                    "priority",
                    "normal",
                ),
            ),
        )

        return context


    def subscribe(self, context):

        payload = context.payload

        context.add_result(
            "subscription",
            self.runtime.event_bus_v3.subscribe(
                topic=payload.get(
                    "topic",
                    "",
                ),
                subscriber=payload.get(
                    "subscriber",
                    "",
                ),
            ),
        )

        return context


    def unsubscribe(self, context):

        payload = context.payload

        context.add_result(
            "subscription",
            self.runtime.event_bus_v3.unsubscribe(
                topic=payload.get(
                    "topic",
                    "",
                ),
                subscriber=payload.get(
                    "subscriber",
                    "",
                ),
            ),
        )

        return context


    def history(self, context):

        context.add_result(
            "history",
            self.runtime.event_bus_v3.history(
                context.payload.get(
                    "topic"
                )
            ),
        )

        return context


    def replay(self, context):

        context.add_result(
            "replay",
            self.runtime.event_bus_v3.replay(
                context.payload.get(
                    "topic",
                    "",
                )
            ),
        )

        return context


    def statistics(self, context):

        context.add_result(
            "event_stats",
            self.runtime.event_bus_v3.statistics(),
        )

        return context
PY



echo "Updating core.py..."

python - <<'PY'
from pathlib import Path

path = Path(
    "aletheus/runtime/core.py"
)

text = path.read_text()


line = (
    "from aletheus.runtime.adapters.event_adapter "
    "import EventCommandAdapter"
)


if line not in text:

    marker = (
        "from aletheus.runtime.adapters.mission_adapter "
        "import MissionCommandAdapter"
    )

    text = text.replace(
        marker,
        marker + "\n" + line
    )


if "self.event_adapter = EventCommandAdapter(self)" not in text:

    marker = (
        "self.mission_adapter = MissionCommandAdapter(self)"
    )

    text = text.replace(
        marker,
        marker + "\n        self.event_adapter = EventCommandAdapter(self)"
    )


path.write_text(text)

PY



echo "Updating event command registration..."


cat > aletheus/runtime/registrations/event_commands.py <<'PY'
"""
Event Command Registration

Genesis 7

Uses EventCommandAdapter boundary.
"""


def register_event_commands(runtime):

    commands = runtime.commands


    commands.register(
        "event.bootstrap",
        runtime.event_adapter.bootstrap,
    )


    commands.register(
        "event.publish",
        runtime.event_adapter.publish,
    )


    commands.register(
        "event.subscribe",
        runtime.event_adapter.subscribe,
    )


    commands.register(
        "event.unsubscribe",
        runtime.event_adapter.unsubscribe,
    )


    commands.register(
        "event.history",
        runtime.event_adapter.history,
    )


    commands.register(
        "event.replay",
        runtime.event_adapter.replay,
    )


    commands.register(
        "event.statistics",
        runtime.event_adapter.statistics,
    )
PY



echo "Compile validation..."

python -m compileall aletheus/runtime



python - <<'PY'
from aletheus.runtime import runtime_core


print(
    {
        "commands":
            runtime_core.commands.count(),

        "graph_adapter":
            type(
                runtime_core.graph_adapter
            ).__name__,

        "mission_adapter":
            type(
                runtime_core.mission_adapter
            ).__name__,

        "event_adapter":
            type(
                runtime_core.event_adapter
            ).__name__,

        "genesis6":
            runtime_core.genesis6_validate()["passed"],

        "freeze":
            runtime_core.genesis6_freeze_review()["approved"]
    }
)

PY


echo "=== Genesis 7 Event Adapter Complete ==="


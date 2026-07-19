#!/bin/bash

set -e

echo "=== Genesis 7 Compatibility Adapter Extraction ==="


mkdir -p aletheus/runtime/adapters


cat > aletheus/runtime/adapters/compatibility_adapter.py <<'PY'
"""
Compatibility Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns compatibility layer command execution.
"""


class CompatibilityCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def list(self, context):

        context.add_result(
            "compatibility",
            self.runtime.compat.list(),
        )

        return context


    def statistics(self, context):

        context.add_result(
            "compatibility_statistics",
            self.runtime.compat.statistics(),
        )

        return context


    def resolve(self, context):

        payload = context.payload

        context.add_result(
            "compatibility_resolution",
            self.runtime.compat.resolve(
                payload.get(
                    "capability",
                    "",
                )
            ),
        )

        return context


    def contract(self, context):

        payload = context.payload

        context.add_result(
            "compatibility_contract",
            self.runtime.compat.contract(
                payload.get(
                    "name",
                    "",
                )
            ),
        )

        return context
PY



echo "Updating core.py imports..."

python - <<'PY'
from pathlib import Path

path = Path(
    "aletheus/runtime/core.py"
)

text = path.read_text()


line = (
    "from aletheus.runtime.adapters.compatibility_adapter "
    "import CompatibilityCommandAdapter"
)


if line not in text:

    marker = (
        "from aletheus.runtime.adapters.runtime_adapter "
        "import RuntimeCommandAdapter"
    )

    text = text.replace(
        marker,
        marker + "\n" + line
    )


if "self.compatibility_adapter = CompatibilityCommandAdapter(self)" not in text:

    marker = (
        "self.runtime_adapter = RuntimeCommandAdapter(self)"
    )

    text = text.replace(
        marker,
        marker + "\n        self.compatibility_adapter = CompatibilityCommandAdapter(self)"
    )


path.write_text(text)

PY



echo "Updating compatibility registration..."


cat > aletheus/runtime/registrations/compatibility_commands.py <<'PY'
"""
Compatibility Command Registration

Genesis 7

Uses CompatibilityCommandAdapter boundary.
"""


def register_compatibility_commands(runtime):

    commands = runtime.commands


    commands.register(
        "compat.list",
        runtime.compatibility_adapter.list,
    )


    commands.register(
        "compat.statistics",
        runtime.compatibility_adapter.statistics,
    )


    commands.register(
        "compat.resolve",
        runtime.compatibility_adapter.resolve,
    )


    commands.register(
        "compat.contract",
        runtime.compatibility_adapter.contract,
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

        "graph":
            type(runtime_core.graph_adapter).__name__,

        "mission":
            type(runtime_core.mission_adapter).__name__,

        "event":
            type(runtime_core.event_adapter).__name__,

        "runtime":
            type(runtime_core.runtime_adapter).__name__,

        "compatibility":
            type(runtime_core.compatibility_adapter).__name__,

        "genesis6":
            runtime_core.genesis6_validate()["passed"],

        "freeze":
            runtime_core.genesis6_freeze_review()["approved"]
    }
)

PY


echo "=== Genesis 7 Compatibility Adapter Complete ==="


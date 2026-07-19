#!/bin/bash

set -e

echo "=== Genesis 7 Runtime Adapter Extraction ==="


mkdir -p aletheus/runtime/adapters


cat > aletheus/runtime/adapters/runtime_adapter.py <<'PY'
"""
Runtime Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns runtime inspection and operational commands.
"""


class RuntimeCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def selftest(self, context):

        context.add_result(
            "selftest",
            self.runtime.certify_runtime(),
        )

        return context


    def dashboard(self, context):

        context.add_result(
            "dashboard",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "commands": self.runtime.commands.count(),
            },
        )

        return context


    def snapshot(self, context):

        context.add_result(
            "snapshot",
            self.runtime.runtime_readiness(),
        )

        return context


    def audit(self, context):

        context.add_result(
            "audit",
            {
                "health": self.runtime.health(),
                "registry": self.runtime.registry_snapshot(),
                "architecture": self.runtime.architecture_validate(),
            },
        )

        return context


    def docs(self, context):

        context.add_result(
            "docs",
            self.runtime.generate_release_manifest(),
        )

        return context


    def doctor(self, context):

        context.add_result(
            "doctor",
            self.runtime.diagnostics(),
        )

        return context


    def invariants(self, context):

        context.add_result(
            "invariants",
            self.runtime.invariants(),
        )

        return context


    def boot_validate(self, context):

        context.add_result(
            "boot_validation",
            self.runtime.boot_certification_validate(),
        )

        return context


    def health_report(self, context):

        context.add_result(
            "health_report",
            self.runtime.health(),
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
    "from aletheus.runtime.adapters.runtime_adapter "
    "import RuntimeCommandAdapter"
)


if line not in text:

    marker = (
        "from aletheus.runtime.adapters.event_adapter "
        "import EventCommandAdapter"
    )

    text = text.replace(
        marker,
        marker + "\n" + line
    )


if "self.runtime_adapter = RuntimeCommandAdapter(self)" not in text:

    marker = (
        "self.event_adapter = EventCommandAdapter(self)"
    )

    text = text.replace(
        marker,
        marker + "\n        self.runtime_adapter = RuntimeCommandAdapter(self)"
    )


path.write_text(text)

PY



echo "Updating runtime command registration..."


cat > aletheus/runtime/registrations/runtime_commands.py <<'PY'
"""
Runtime Command Registration

Genesis 7

Uses RuntimeCommandAdapter boundary.
"""


def register_runtime_commands(runtime):

    commands = runtime.commands


    commands.register(
        "runtime.selftest",
        runtime.runtime_adapter.selftest,
    )


    commands.register(
        "runtime.dashboard",
        runtime.runtime_adapter.dashboard,
    )


    commands.register(
        "runtime.snapshot",
        runtime.runtime_adapter.snapshot,
    )


    commands.register(
        "runtime.audit",
        runtime.runtime_adapter.audit,
    )


    commands.register(
        "runtime.docs",
        runtime.runtime_adapter.docs,
    )


    commands.register(
        "runtime.doctor",
        runtime.runtime_adapter.doctor,
    )


    commands.register(
        "runtime.invariants",
        runtime.runtime_adapter.invariants,
    )


    commands.register(
        "runtime.boot.validate",
        runtime.runtime_adapter.boot_validate,
    )


    commands.register(
        "runtime.health",
        runtime.runtime_adapter.health_report,
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
            type(runtime_core.graph_adapter).__name__,

        "mission_adapter":
            type(runtime_core.mission_adapter).__name__,

        "event_adapter":
            type(runtime_core.event_adapter).__name__,

        "runtime_adapter":
            type(runtime_core.runtime_adapter).__name__,

        "genesis6":
            runtime_core.genesis6_validate()["passed"],

        "freeze":
            runtime_core.genesis6_freeze_review()["approved"]
    }
)
PY


echo "=== Genesis 7 Runtime Adapter Complete ==="


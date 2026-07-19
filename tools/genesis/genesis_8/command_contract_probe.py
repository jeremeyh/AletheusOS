from __future__ import annotations

import inspect
from pathlib import Path
from pprint import pformat
from typing import Any

from aletheus.runtime import runtime_core


COMMANDS = (
    "plugin.bootstrap",
    "plugin.install",
    "plugin.statistics",
    "kernel.bootstrap",
    "kernel.execute",
    "kernel.tasks",
    "kernel.scheduler",
    "kernel.dispatcher",
    "kernel.supervisor",
    "kernel.statistics",
    "runtime.doctor",
    "runtime.invariants",
    "runtime.boot.validate",
    "runtime.health_report",
)


def handler_name(handler: Any) -> str:
    return (
        f"{getattr(handler, '__module__', type(handler).__module__)}."
        f"{getattr(handler, '__qualname__', type(handler).__qualname__)}"
    )


def source_location(handler: Any) -> str:
    try:
        path = inspect.getsourcefile(handler)
        line = inspect.getsourcelines(handler)[1]
    except (TypeError, OSError):
        return "unknown"

    return f"{path}:{line}"


def safe_signature(handler: Any) -> str:
    try:
        return str(inspect.signature(handler))
    except (TypeError, ValueError):
        return "unknown"


def main() -> None:
    registry = runtime_core.commands.registry
    dispatcher = registry.dispatcher

    lines = [
        "# Genesis 8 Command Contract Probe",
        "",
        f"- Registered commands: {registry.count()}",
        f"- Generation: {registry.generation}",
        f"- Fingerprint: `{registry.fingerprint}`",
        "",
    ]

    for name in COMMANDS:
        record = registry.get(name)

        lines.extend(
            [
                f"## `{name}`",
                "",
                f"- Registered: **{record is not None}**",
            ]
        )

        if record is None:
            lines.append("")
            continue

        handler = record.handler

        lines.extend(
            [
                f"- Handler: `{handler_name(handler)}`",
                f"- Location: `{source_location(handler)}`",
                f"- Signature: `{safe_signature(handler)}`",
                f"- Invocation mode: `{dispatcher.invocation_mode(name)}`",
                f"- Category: `{record.category}`",
                f"- Description: `{record.description}`",
                f"- Metadata: `{pformat(record.metadata)}`",
                "",
            ]
        )

        try:
            source = inspect.getsource(handler)
        except (TypeError, OSError):
            source = "<source unavailable>"

        lines.extend(
            [
                "```python",
                source.rstrip(),
                "```",
                "",
            ]
        )

    report = Path(
        "reports/genesis_8_command_dispatch/"
        "command_contract_probe.md"
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines), encoding="utf-8")

    print(f"Report: {report}")
    print()
    print("Summary:")

    for name in COMMANDS:
        record = registry.get(name)

        if record is None:
            print(f"- {name}: MISSING")
            continue

        print(
            f"- {name}: "
            f"{handler_name(record.handler)} "
            f"mode={dispatcher.invocation_mode(name)} "
            f"metadata={record.metadata}"
        )


if __name__ == "__main__":
    main()

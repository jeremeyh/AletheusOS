#!/usr/bin/env python3
"""
Genesis 7 Runtime Identity and Ownership Audit

Determines whether overlapping runtime attachments are:

- aliases to the same object,
- separate instances of the same implementation,
- or separate implementations with related names.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from aletheus.runtime import runtime_core


REPORT_DIR = Path("reports/genesis_7_architecture_audit")
REPORT_PATH = REPORT_DIR / "runtime_identity_audit.txt"


GROUPS = {
    "agents": [
        "agents",
        "agents_v2",
    ],
    "event_system": [
        "event_bus",
        "event_bus_v3",
        "events",
    ],
    "high_availability": [
        "high_availability",
        "high_availability_v3",
    ],
    "kernel": [
        "kernel",
        "kernel_v2",
    ],
    "mission": [
        "mission",
        "mission_v2",
    ],
    "planning": [
        "planning",
        "planning_v2",
    ],
    "plugins": [
        "plugins",
        "plugins_v3",
    ],
    "security": [
        "security",
        "security_v3",
    ],
    "services": [
        "services",
        "service_registry",
    ],
    "tenancy": [
        "tenancy",
        "tenancy_v3",
    ],
    "workflow": [
        "workflow",
        "workflow_v2",
        "workflow_v3",
        "workflows",
    ],
}


def describe(name: str, value: Any) -> dict[str, Any]:
    cls = type(value)

    return {
        "name": name,
        "type": cls.__name__,
        "module": cls.__module__,
        "object_id": id(value),
    }


def relationship(
    left_name: str,
    left: Any,
    right_name: str,
    right: Any,
) -> str:
    if left is right:
        return "SAME_OBJECT_ALIAS"

    if type(left) is type(right):
        return "DISTINCT_INSTANCES_SAME_TYPE"

    return "DISTINCT_IMPLEMENTATIONS"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "Genesis 7 Runtime Identity and Ownership Audit",
        "=" * 78,
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Runtime: {type(runtime_core).__name__}",
        "",
    ]

    summary = {
        "same_object_aliases": 0,
        "distinct_same_type": 0,
        "distinct_implementations": 0,
        "missing": 0,
    }

    for group_name, names in GROUPS.items():
        lines.extend(
            [
                f"[{group_name.upper()}]",
                "-" * 78,
            ]
        )

        available: list[tuple[str, Any]] = []

        for name in names:
            if not hasattr(runtime_core, name):
                summary["missing"] += 1
                lines.append(f"{name:28} MISSING")
                continue

            value = getattr(runtime_core, name)
            info = describe(name, value)
            available.append((name, value))

            lines.append(
                f"{name:28} "
                f"type={info['type']:34} "
                f"module={info['module']} "
                f"id={info['object_id']}"
            )

        lines.append("")
        lines.append("Relationships:")

        if len(available) < 2:
            lines.append("  Insufficient members for comparison.")
        else:
            for index, (left_name, left) in enumerate(available):
                for right_name, right in available[index + 1:]:
                    result = relationship(
                        left_name,
                        left,
                        right_name,
                        right,
                    )

                    if result == "SAME_OBJECT_ALIAS":
                        summary["same_object_aliases"] += 1
                    elif result == "DISTINCT_INSTANCES_SAME_TYPE":
                        summary["distinct_same_type"] += 1
                    else:
                        summary["distinct_implementations"] += 1

                    lines.append(
                        f"  {left_name:24} <-> "
                        f"{right_name:24} {result}"
                    )

        lines.append("")

    lines.extend(
        [
            "=" * 78,
            "Summary",
            "-" * 78,
            (
                "Same-object alias relationships: "
                f"{summary['same_object_aliases']}"
            ),
            (
                "Distinct instances of same type: "
                f"{summary['distinct_same_type']}"
            ),
            (
                "Distinct implementations: "
                f"{summary['distinct_implementations']}"
            ),
            f"Missing attachments: {summary['missing']}",
            "",
            "Interpretation",
            "-" * 78,
            (
                "SAME_OBJECT_ALIAS: Low immediate risk. Preserve temporarily "
                "and select one canonical public name."
            ),
            (
                "DISTINCT_INSTANCES_SAME_TYPE: Review required. Separate state "
                "may drift even though implementation types match."
            ),
            (
                "DISTINCT_IMPLEMENTATIONS: Explicit ownership boundaries or "
                "retirement plans are required."
            ),
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "Same-object aliases:",
        summary["same_object_aliases"],
    )
    print(
        "Distinct same-type instances:",
        summary["distinct_same_type"],
    )
    print(
        "Distinct implementations:",
        summary["distinct_implementations"],
    )
    print("Missing:", summary["missing"])
    print("Report:", REPORT_PATH)


if __name__ == "__main__":
    main()

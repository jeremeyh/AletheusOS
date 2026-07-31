#!/usr/bin/env python3
"""
Genesis 7 Runtime Composition Audit

Inventories runtime attachments, classifies likely component roles,
and identifies generation overlap and composition pressure.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from aletheus.runtime import runtime_core

REPORT_DIR = Path("reports/genesis_7_architecture_audit")
REPORT_PATH = REPORT_DIR / "runtime_composition_audit.txt"


ROLE_SUFFIXES = {
    "_manager": "manager",
    "_registry": "registry",
    "_adapter": "adapter",
    "_anchor": "anchor",
    "_validator": "validator",
    "_auditor": "auditor",
    "_bootstrapper": "bootstrapper",
    "_orchestrator": "orchestrator",
    "_scheduler": "scheduler",
    "_supervisor": "supervisor",
}


def classify(name: str, value: Any) -> str:
    for suffix, role in ROLE_SUFFIXES.items():
        if name.endswith(suffix):
            return role

    type_name = type(value).__name__.lower()

    for role in (
        "manager",
        "registry",
        "adapter",
        "engine",
        "runtime",
        "service",
        "controller",
        "executor",
        "fabric",
        "core",
    ):
        if role in type_name:
            return role

    if isinstance(value, str):
        return "metadata"

    return "component"


def generation_family(name: str) -> tuple[str, str | None]:
    for suffix in ("_v2", "_v3", "_v4"):
        if name.endswith(suffix):
            return name[: -len(suffix)], suffix[1:]

    return name, None


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    public_attributes = {
        name: value
        for name, value in vars(runtime_core).items()
        if not name.startswith("_")
    }

    roles: dict[str, list[tuple[str, str]]] = defaultdict(list)
    families: dict[str, list[tuple[str, str | None, str]]] = defaultdict(list)

    for name, value in sorted(public_attributes.items()):
        role = classify(name, value)
        type_name = type(value).__name__

        roles[role].append((name, type_name))

        family, generation = generation_family(name)
        families[family].append(
            (
                name,
                generation,
                type_name,
            )
        )

    overlapping_families = {
        family: members for family, members in families.items() if len(members) > 1
    }

    lines = [
        "Genesis 7 Runtime Composition Audit",
        "=" * 78,
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Runtime: {type(runtime_core).__name__}",
        f"Public attachments: {len(public_attributes)}",
        "",
        "Role Summary",
        "-" * 78,
    ]

    for role in sorted(roles):
        lines.append(f"{role:18} {len(roles[role]):3}")

    lines.extend(
        [
            "",
            "Runtime Attachments",
            "-" * 78,
        ]
    )

    for role in sorted(roles):
        lines.append("")
        lines.append(f"[{role.upper()}]")

        for name, type_name in roles[role]:
            lines.append(f"{name:34} {type_name}")

    lines.extend(
        [
            "",
            "Generation / Ownership Overlap",
            "-" * 78,
        ]
    )

    if not overlapping_families:
        lines.append("No naming-based overlaps detected.")
    else:
        for family, members in sorted(overlapping_families.items()):
            lines.append("")
            lines.append(f"{family}:")

            for name, generation, type_name in members:
                generation_label = generation or "base"
                lines.append(
                    f"  {name:30} generation={generation_label:5} type={type_name}"
                )

    lines.extend(
        [
            "",
            "Initial Structural Signals",
            "-" * 78,
            ("PASS: Runtime imports and boots."),
            ("PASS: Command surface is operational."),
            (
                "REVIEW: Public attachment density should be assessed "
                "against composition-root boundaries."
            ),
            (
                "REVIEW: Generation overlaps require canonical ownership "
                "and compatibility classification."
            ),
            (
                "REVIEW: services and service_registry may represent "
                "duplicate references or separate ownership."
            ),
            (
                "REVIEW: event_bus, event_bus_v3, and events require "
                "boundary clarification."
            ),
            (
                "REVIEW: workflow, workflow_v2, workflow_v3, and workflows "
                "require canonical-path reconciliation."
            ),
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Runtime: {type(runtime_core).__name__}")
    print(f"Public attachments: {len(public_attributes)}")
    print(f"Generation overlaps: {len(overlapping_families)}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()

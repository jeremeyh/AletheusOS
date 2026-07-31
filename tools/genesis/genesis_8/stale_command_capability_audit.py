from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path
from typing import Any

from aletheus.runtime import runtime_core

ROOT = Path(__file__).resolve().parent
REPORT_DIR = ROOT / "reports/genesis_8_command_dispatch"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

JSON_REPORT = REPORT_DIR / "stale_command_capability_audit.json"
MD_REPORT = REPORT_DIR / "stale_command_capability_audit.md"

MODULES = (
    "workspace_commands",
    "application_commands",
    "semantic_commands",
    "executive_commands",
    "planning_commands",
    "uil_commands",
)


def public_members(target: Any) -> list[dict[str, Any]]:
    members = []

    for name in sorted(dir(target)):
        if name.startswith("_"):
            continue

        try:
            value = getattr(target, name)
        except Exception:
            continue

        if callable(value):
            try:
                signature = str(inspect.signature(value))
            except (TypeError, ValueError):
                signature = "(...)"

            kind = "method"
        else:
            signature = None
            kind = type(value).__name__

        members.append(
            {
                "name": name,
                "kind": kind,
                "signature": signature,
            }
        )

    return members


def extract_registration_targets(path: Path) -> list[dict[str, Any]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    commands = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not (isinstance(node.func, ast.Attribute) and node.func.attr == "register"):
            continue

        if len(node.args) < 2:
            continue

        command_node = node.args[0]
        handler_node = node.args[1]

        if not (
            isinstance(command_node, ast.Constant)
            and isinstance(command_node.value, str)
        ):
            continue

        try:
            handler_text = ast.unparse(handler_node)
        except Exception:
            handler_text = "<unknown>"

        commands.append(
            {
                "command": command_node.value,
                "handler_expression": handler_text,
                "line": node.lineno,
            }
        )

    return commands


runtime_members = public_members(runtime_core)

candidate_components = {}

for name in sorted(dir(runtime_core)):
    if name.startswith("_"):
        continue

    try:
        value = getattr(runtime_core, name)
    except Exception:
        continue

    if value is None:
        continue

    if callable(value):
        continue

    module_name = type(value).__module__

    if (
        module_name.startswith("aletheus")
        or name.endswith("_manager")
        or name.endswith("_adapter")
        or name.endswith("_domain")
        or name.endswith("_core")
    ):
        candidate_components[name] = {
            "type": (f"{type(value).__module__}.{type(value).__qualname__}"),
            "members": public_members(value),
        }


records = []

for module_stem in MODULES:
    path = ROOT / "aletheus/runtime/registrations" / f"{module_stem}.py"

    records.append(
        {
            "module": module_stem,
            "file": str(path.relative_to(ROOT)),
            "commands": extract_registration_targets(path),
        }
    )


report = {
    "runtime_type": (
        f"{type(runtime_core).__module__}.{type(runtime_core).__qualname__}"
    ),
    "runtime_public_members": runtime_members,
    "candidate_components": candidate_components,
    "stale_registration_modules": records,
}

JSON_REPORT.write_text(
    json.dumps(report, indent=2, sort_keys=True),
    encoding="utf-8",
)


lines = [
    "# Genesis 8 Stale Command Capability Audit",
    "",
    f"- Runtime type: `{report['runtime_type']}`",
    f"- Candidate components: **{len(candidate_components)}**",
    "",
    "## Stale Registration Modules",
]

for record in records:
    lines.extend(
        [
            "",
            f"### `{record['module']}`",
            "",
        ]
    )

    for command in record["commands"]:
        lines.append(
            f"- `{command['command']}` → "
            f"`{command['handler_expression']}` "
            f"(line {command['line']})"
        )

lines.extend(
    [
        "",
        "## Candidate Runtime Components",
        "",
    ]
)

for name, component in candidate_components.items():
    lines.extend(
        [
            f"### `{name}`",
            "",
            f"- Type: `{component['type']}`",
        ]
    )

    methods = [member for member in component["members"] if member["kind"] == "method"]

    for member in methods:
        lines.append(f"- `{member['name']}{member['signature']}`")

    lines.append("")

MD_REPORT.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("Genesis 8 stale capability audit generated.")
print(f"JSON: {JSON_REPORT.relative_to(ROOT)}")
print(f"Markdown: {MD_REPORT.relative_to(ROOT)}")
print(f"Candidate components: {len(candidate_components)}")

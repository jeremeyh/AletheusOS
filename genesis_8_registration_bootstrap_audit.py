from __future__ import annotations

import ast
import importlib
import inspect
import json
import re
from pathlib import Path
from typing import Any

from aletheus.runtime import runtime_core


ROOT = Path(__file__).resolve().parent
REGISTRATION_DIR = ROOT / "aletheus/runtime/registrations"
RUNTIME_DIR = ROOT / "aletheus/runtime"
REPORT_DIR = ROOT / "reports/genesis_8_command_dispatch"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

JSON_REPORT = REPORT_DIR / "registration_bootstrap_audit.json"
MD_REPORT = REPORT_DIR / "registration_bootstrap_audit.md"


def module_name(path: Path) -> str:
    return ".".join(
        path.relative_to(ROOT).with_suffix("").parts
    )


def extract_registered_commands(
    path: Path,
) -> list[str]:
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except (OSError, SyntaxError, UnicodeDecodeError):
        return []

    commands: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if not (
            isinstance(function, ast.Attribute)
            and function.attr in {
                "register",
                "register_context_handler",
                "register_payload_handler",
            }
        ):
            continue

        if not node.args:
            continue

        command_node = node.args[0]

        if (
            isinstance(command_node, ast.Constant)
            and isinstance(command_node.value, str)
        ):
            commands.append(command_node.value)

    return sorted(set(commands))


def registration_functions(path: Path) -> list[str]:
    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
    except (OSError, SyntaxError, UnicodeDecodeError):
        return []

    return sorted(
        node.name
        for node in tree.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
        and node.name.startswith("register_")
    )


def source_mentions(
    qualified_module: str,
    function_name: str,
) -> list[str]:
    references: list[str] = []
    module_tail = qualified_module.rsplit(".", 1)[-1]

    patterns = (
        qualified_module,
        f"from {qualified_module} import",
        f"import {qualified_module}",
        function_name,
        module_tail,
    )

    for path in RUNTIME_DIR.rglob("*.py"):
        if path.parent == REGISTRATION_DIR:
            continue

        path_text = str(path)

        if any(
            marker in path_text
            for marker in (
                "__pycache__",
                ".backup",
                "before_",
                "restored",
            )
        ):
            continue

        try:
            lines = path.read_text(
                encoding="utf-8"
            ).splitlines()
        except (OSError, UnicodeDecodeError):
            continue

        for line_number, line in enumerate(lines, start=1):
            if any(pattern in line for pattern in patterns):
                references.append(
                    f"{path.relative_to(ROOT)}:{line_number}:"
                    f"{line.strip()}"
                )

    return references[:30]


live_commands = set(runtime_core.commands.registry.list())
records: list[dict[str, Any]] = []

for path in sorted(REGISTRATION_DIR.glob("*_commands.py")):
    module = module_name(path)
    functions = registration_functions(path)
    declared = extract_registered_commands(path)
    live = sorted(set(declared) & live_commands)
    missing = sorted(set(declared) - live_commands)

    function_references: dict[str, list[str]] = {
        function: source_mentions(module, function)
        for function in functions
    }

    likely_called = any(
        references
        for references in function_references.values()
    )

    import_error = None

    try:
        imported = importlib.import_module(module)
        loadable_functions = [
            function
            for function in functions
            if callable(getattr(imported, function, None))
        ]
    except Exception as exc:
        import_error = f"{type(exc).__name__}: {exc}"
        loadable_functions = []

    records.append(
        {
            "file": str(path.relative_to(ROOT)),
            "module": module,
            "registration_functions": functions,
            "loadable_functions": loadable_functions,
            "declared_commands": declared,
            "live_commands": live,
            "missing_commands": missing,
            "all_declared_live": bool(declared)
            and not missing,
            "likely_referenced_by_bootstrap": likely_called,
            "references": function_references,
            "import_error": import_error,
        }
    )


summary = {
    "registration_modules": len(records),
    "fully_live_modules": sum(
        1 for record in records
        if record["all_declared_live"]
    ),
    "partially_or_fully_missing_modules": sum(
        1 for record in records
        if record["missing_commands"]
    ),
    "unreferenced_missing_modules": sum(
        1 for record in records
        if record["missing_commands"]
        and not record["likely_referenced_by_bootstrap"]
    ),
    "modules_with_import_errors": sum(
        1 for record in records
        if record["import_error"]
    ),
}

JSON_REPORT.write_text(
    json.dumps(
        {
            "summary": summary,
            "modules": records,
        },
        indent=2,
        sort_keys=True,
    ),
    encoding="utf-8",
)

lines = [
    "# Genesis 8 Registration Bootstrap Audit",
    "",
    "## Summary",
    "",
]

for key, value in summary.items():
    lines.append(f"- {key}: **{value}**")

for record in records:
    if not record["missing_commands"]:
        continue

    lines.extend(
        [
            "",
            f"## `{record['module']}`",
            "",
            f"- File: `{record['file']}`",
            (
                "- Functions: "
                + ", ".join(
                    f"`{name}`"
                    for name in record[
                        "registration_functions"
                    ]
                )
            ),
            (
                "- Loadable functions: "
                + ", ".join(
                    f"`{name}`"
                    for name in record[
                        "loadable_functions"
                    ]
                )
            ),
            (
                "- Missing commands: "
                + ", ".join(
                    f"`{name}`"
                    for name in record[
                        "missing_commands"
                    ]
                )
            ),
            (
                "- Referenced by bootstrap: "
                f"`{record['likely_referenced_by_bootstrap']}`"
            ),
        ]
    )

    if record["import_error"]:
        lines.append(
            f"- Import error: `{record['import_error']}`"
        )

    for function, references in record["references"].items():
        if not references:
            continue

        lines.append(f"- References for `{function}`:")

        for reference in references:
            lines.append(f"  - `{reference}`")

MD_REPORT.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("Genesis 8 registration bootstrap audit generated.")
print(f"JSON: {JSON_REPORT.relative_to(ROOT)}")
print(f"Markdown: {MD_REPORT.relative_to(ROOT)}")
print()

for key, value in summary.items():
    print(f"{key}: {value}")

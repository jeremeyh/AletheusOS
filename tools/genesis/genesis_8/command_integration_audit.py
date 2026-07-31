from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

TARGETS = {
    "command_bus": ROOT / "aletheus/runtime/commands/command_bus.py",
    "command_package": ROOT / "aletheus/runtime/commands/__init__.py",
    "registry": ROOT / "aletheus/runtime/commands_v2/registry.py",
    "command_manager": ROOT / "aletheus/runtime/managers/command_manager.py",
    "runtime_core": ROOT / "aletheus/runtime/core.py",
}

REPORT_DIR = ROOT / "reports/genesis_8_command_dispatch"
REPORT_PATH = REPORT_DIR / "command_integration_audit.md"
JSON_PATH = REPORT_DIR / "command_integration_audit.json"


def qualified_name(node: ast.expr | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = qualified_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Subscript):
        return qualified_name(node.value)
    return ast.dump(node, include_attributes=False)


def annotation_name(node: ast.expr | None) -> str:
    return qualified_name(node)


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args: list[str] = []

    positional = [*node.args.posonlyargs, *node.args.args]
    defaults_offset = len(positional) - len(node.args.defaults)

    for index, arg in enumerate(positional):
        text = arg.arg
        annotation = annotation_name(arg.annotation)
        if annotation:
            text += f": {annotation}"

        if index >= defaults_offset:
            default = node.args.defaults[index - defaults_offset]
            text += f" = {ast.unparse(default)}"

        args.append(text)

    if node.args.vararg:
        text = f"*{node.args.vararg.arg}"
        annotation = annotation_name(node.args.vararg.annotation)
        if annotation:
            text += f": {annotation}"
        args.append(text)
    elif node.args.kwonlyargs:
        args.append("*")

    for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults):
        text = arg.arg
        annotation = annotation_name(arg.annotation)
        if annotation:
            text += f": {annotation}"
        if default is not None:
            text += f" = {ast.unparse(default)}"
        args.append(text)

    if node.args.kwarg:
        text = f"**{node.args.kwarg.arg}"
        annotation = annotation_name(node.args.kwarg.annotation)
        if annotation:
            text += f": {annotation}"
        args.append(text)

    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    result = f"{prefix} {node.name}({', '.join(args)})"

    return_annotation = annotation_name(node.returns)
    if return_annotation:
        result += f" -> {return_annotation}"

    return result


def analyze_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "exists": False,
            "path": str(path.relative_to(ROOT)),
        }

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    imports: list[str] = []
    classes: list[dict[str, Any]] = []
    top_level_functions: list[str] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for item in node.names:
                imports.append(f"import {item.name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(item.name for item in node.names)
            imports.append(f"from {module} import {names}")
        elif isinstance(node, ast.ClassDef):
            methods: list[str] = []
            attributes: list[str] = []

            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append(function_signature(child))
                elif isinstance(child, ast.AnnAssign):
                    if isinstance(child.target, ast.Name):
                        attributes.append(child.target.id)
                elif isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name):
                            attributes.append(target.id)

            classes.append(
                {
                    "name": node.name,
                    "bases": [qualified_name(base) for base in node.bases],
                    "methods": methods,
                    "attributes": sorted(set(attributes)),
                }
            )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            top_level_functions.append(function_signature(node))

    return {
        "exists": True,
        "path": str(path.relative_to(ROOT)),
        "line_count": len(source.splitlines()),
        "imports": imports,
        "classes": classes,
        "functions": top_level_functions,
    }


def find_command_references() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for path in sorted((ROOT / "aletheus").rglob("*.py")):
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        relevant_lines = []
        for line_number, line in enumerate(source.splitlines(), start=1):
            if any(
                token in line
                for token in (
                    "CommandBus",
                    ".command_bus",
                    ".dispatch(",
                    ".execute(",
                    ".register(",
                    "register_context_handler",
                    "RuntimeCommandRegistry",
                    "CommandManager",
                )
            ):
                relevant_lines.append(
                    {
                        "line": line_number,
                        "text": line.strip(),
                    }
                )

        if relevant_lines:
            results.append(
                {
                    "path": str(path.relative_to(ROOT)),
                    "references": relevant_lines,
                }
            )

    return results


def render_report(
    analyses: dict[str, dict[str, Any]],
    references: list[dict[str, Any]],
) -> str:
    lines = [
        "# Genesis 8 Command Integration Audit",
        "",
        "## Objective",
        "",
        "Map the existing command façade, registry, manager, and runtime call sites",
        "before wiring the Genesis 8 dispatcher behind the stable `CommandBus` API.",
        "",
    ]

    for name, data in analyses.items():
        lines.extend(
            [
                f"## {name}",
                "",
                f"- Path: `{data['path']}`",
                f"- Exists: **{data['exists']}**",
            ]
        )

        if not data["exists"]:
            lines.append("")
            continue

        lines.extend(
            [
                f"- Lines: **{data['line_count']}**",
                "",
                "### Imports",
                "",
            ]
        )

        for item in data["imports"]:
            lines.append(f"- `{item}`")

        if not data["imports"]:
            lines.append("- None")

        lines.extend(["", "### Classes", ""])

        for class_info in data["classes"]:
            bases = ", ".join(class_info["bases"]) or "object"
            lines.extend(
                [
                    f"#### `{class_info['name']}({bases})`",
                    "",
                    "Methods:",
                    "",
                ]
            )

            for method in class_info["methods"]:
                lines.append(f"- `{method}`")

            if not class_info["methods"]:
                lines.append("- None")

            if class_info["attributes"]:
                lines.extend(["", "Attributes:", ""])
                for attribute in class_info["attributes"]:
                    lines.append(f"- `{attribute}`")

            lines.append("")

        if not data["classes"]:
            lines.append("- None")
            lines.append("")

        lines.extend(["### Top-level functions", ""])

        for function in data["functions"]:
            lines.append(f"- `{function}`")

        if not data["functions"]:
            lines.append("- None")

        lines.append("")

    lines.extend(
        [
            "## Command References",
            "",
        ]
    )

    for result in references:
        lines.append(f"### `{result['path']}`")
        lines.append("")

        for reference in result["references"]:
            lines.append(f"- L{reference['line']}: `{reference['text']}`")

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    analyses = {name: analyze_file(path) for name, path in TARGETS.items()}
    references = find_command_references()

    payload = {
        "targets": analyses,
        "references": references,
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    REPORT_PATH.write_text(
        render_report(analyses, references),
        encoding="utf-8",
    )

    print("Genesis 8 command integration audit complete.")
    print(f"Report: {REPORT_PATH.relative_to(ROOT)}")
    print(f"JSON:   {JSON_PATH.relative_to(ROOT)}")

    print("\nDetected components:")
    for name, analysis in analyses.items():
        state = "FOUND" if analysis["exists"] else "MISSING"
        print(f"- {name}: {state} ({analysis['path']})")

    print(f"\nFiles containing command references: {len(references)}")


if __name__ == "__main__":
    main()

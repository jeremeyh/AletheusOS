from pathlib import Path
import ast


PATH = Path(
    "aletheus/runtime/command_bootstrap/bootstrapper.py"
)

text = PATH.read_text(encoding="utf-8")

import_line = (
    "from aletheus.runtime.registrations.workflow_commands "
    "import register_workflow_commands\n"
)


# ---------------------------------------------------------
# Add import
# ---------------------------------------------------------

if import_line not in text:
    registration_imports = [
        node
        for node in ast.parse(text).body
        if isinstance(node, ast.ImportFrom)
        and node.module
        and node.module.startswith(
            "aletheus.runtime.registrations."
        )
    ]

    if not registration_imports:
        raise RuntimeError(
            "Could not locate registration import section."
        )

    final_import = max(
        registration_imports,
        key=lambda node: node.end_lineno,
    )

    lines = text.splitlines(keepends=True)
    insert_at = final_import.end_lineno

    lines.insert(
        insert_at,
        import_line,
    )

    text = "".join(lines)


# ---------------------------------------------------------
# Add registrar to guarded compatibility catalog
# ---------------------------------------------------------

tree = ast.parse(text)

catalog = None

for node in ast.walk(tree):
    target_name = None

    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                target_name = target.id

    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            target_name = node.target.id

    if (
        target_name == "LEGACY_REGISTRATION_FUNCTIONS"
        and isinstance(node.value, ast.Tuple)
    ):
        catalog = node.value
        break

if catalog is None:
    raise RuntimeError(
        "LEGACY_REGISTRATION_FUNCTIONS tuple was not found."
    )

catalog_source = ast.get_source_segment(
    text,
    catalog,
)

if catalog_source is None:
    raise RuntimeError(
        "Could not read registration catalog source."
    )

if "register_workflow_commands" not in catalog_source:
    closing = catalog.end_col_offset - 1

    lines = text.splitlines(keepends=True)
    closing_line_index = catalog.end_lineno - 1
    closing_line = lines[closing_line_index]

    indent = (
        closing_line[
            : len(closing_line)
            - len(closing_line.lstrip())
        ]
        + "    "
    )

    lines.insert(
        closing_line_index,
        f"{indent}register_workflow_commands,\n",
    )

    text = "".join(lines)


PATH.write_text(
    text,
    encoding="utf-8",
)

print(
    "Legacy workflow registrar added to bootstrap catalog."
)

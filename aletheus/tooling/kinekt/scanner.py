"""Static Python repository scanner."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path, PurePosixPath

from .configuration import KinektConfiguration
from .models import DefinitionRecord, ModuleRecord
from .ownership import infer_owner


def _module_name(root: Path, path: Path) -> str:
    relative = path.relative_to(root).with_suffix("")
    parts = list(relative.parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _package_name(module: str) -> str:
    parts = module.split(".")
    if len(parts) >= 2 and parts[0] == "aletheus":
        return ".".join(parts[:2])
    return parts[0] if parts else "root"


def _fingerprint(node: ast.AST) -> str:
    normalized = ast.dump(node, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _branch_count(node: ast.AST) -> int:
    branch_types = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.Match)
    return sum(isinstance(child, branch_types) for child in ast.walk(node))


def _definition(
    module: str,
    relative_path: PurePosixPath,
    node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
) -> DefinitionRecord:
    kind = "class" if isinstance(node, ast.ClassDef) else "function"
    return DefinitionRecord(
        module=module,
        path=relative_path.as_posix(),
        kind=kind,
        name=node.name,
        qualified_name=f"{module}.{node.name}",
        line=node.lineno,
        end_line=getattr(node, "end_lineno", node.lineno),
        fingerprint=_fingerprint(node),
        has_docstring=ast.get_docstring(node) is not None,
        statement_count=sum(isinstance(child, ast.stmt) for child in ast.walk(node)),
        branch_count=_branch_count(node),
    )


def scan_repository(configuration: KinektConfiguration) -> list[ModuleRecord]:
    modules: list[ModuleRecord] = []
    root = configuration.root.resolve()

    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        if any(part in configuration.excluded_parts for part in relative.parts):
            continue

        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        module = _module_name(root, path)
        imports: set[str] = set()
        definitions: list[DefinitionRecord] = []

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError:
            modules.append(
                ModuleRecord(
                    module=module,
                    path=relative.as_posix(),
                    package=_package_name(module),
                    owner=infer_owner(PurePosixPath(relative.as_posix())),
                    lines=len(source.splitlines()),
                    imports=(),
                    definitions=(),
                    syntax_valid=False,
                )
            )
            continue

        for node in tree.body:
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(
                node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                definitions.append(
                    _definition(
                        module,
                        PurePosixPath(relative.as_posix()),
                        node,
                    )
                )

        modules.append(
            ModuleRecord(
                module=module,
                path=relative.as_posix(),
                package=_package_name(module),
                owner=infer_owner(PurePosixPath(relative.as_posix())),
                lines=len(source.splitlines()),
                imports=tuple(sorted(imports)),
                definitions=tuple(definitions),
            )
        )

    return modules

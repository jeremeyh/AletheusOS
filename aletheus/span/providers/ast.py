"""Python AST discovery provider for SPAN™."""

from __future__ import annotations

import ast
from pathlib import Path

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext


def _qualified_name(module: str, local_name: str) -> str:
    return f"{module}.{local_name}" if module else local_name


def _module_name(relative: Path) -> str:
    without_suffix = relative.with_suffix("")
    parts = list(without_suffix.parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _decorator_name(node: ast.expr) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return node.__class__.__name__


class ASTProvider(Provider):
    name = "ast"
    version = "1.0.0"
    description = "Collect Python symbols, inheritance, decorators, and syntax errors."

    def __init__(self, *, include_tests: bool = True) -> None:
        self.include_tests = include_tests

    def collect(self, context: ProviderContext):
        root = context.root.resolve()
        for path in sorted(root.rglob("*.py")):
            relative = path.relative_to(root)
            if any(part in {".git", ".venv", "venv", "__pycache__"} for part in relative.parts):
                continue
            if not self.include_tests and "tests" in relative.parts:
                continue

            module = _module_name(relative)
            try:
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source, filename=str(path))
            except (OSError, UnicodeDecodeError, SyntaxError) as exc:
                yield EvidenceRecord(
                    kind="syntax_error",
                    provider=self.name,
                    source=relative.as_posix(),
                    location=str(path),
                    confidence=1.0,
                    payload={
                        "module": module,
                        "error_type": exc.__class__.__name__,
                        "message": str(exc),
                    },
                    tags=("python", "ast", "error"),
                )
                continue

            yield EvidenceRecord(
                kind="python_module",
                provider=self.name,
                source=relative.as_posix(),
                location=str(path),
                payload={
                    "module": module,
                    "path": relative.as_posix(),
                    "docstring": ast.get_docstring(tree),
                },
                tags=("python", "ast", "module"),
            )

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    yield EvidenceRecord(
                        kind="function",
                        provider=self.name,
                        source=relative.as_posix(),
                        location=f"{path}:{node.lineno}",
                        payload={
                            "module": module,
                            "name": node.name,
                            "qualified_name": _qualified_name(module, node.name),
                            "line": node.lineno,
                            "async": isinstance(node, ast.AsyncFunctionDef),
                            "decorators": [_decorator_name(item) for item in node.decorator_list],
                            "docstring": ast.get_docstring(node),
                        },
                        tags=("python", "ast", "function"),
                    )

                elif isinstance(node, ast.ClassDef):
                    bases = []
                    for base in node.bases:
                        try:
                            bases.append(ast.unparse(base))
                        except Exception:
                            bases.append(base.__class__.__name__)
                    yield EvidenceRecord(
                        kind="class",
                        provider=self.name,
                        source=relative.as_posix(),
                        location=f"{path}:{node.lineno}",
                        payload={
                            "module": module,
                            "name": node.name,
                            "qualified_name": _qualified_name(module, node.name),
                            "line": node.lineno,
                            "bases": bases,
                            "decorators": [_decorator_name(item) for item in node.decorator_list],
                            "docstring": ast.get_docstring(node),
                        },
                        tags=("python", "ast", "class"),
                    )

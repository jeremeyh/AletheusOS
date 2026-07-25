from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


@dataclass(slots=True)
class ProjectContext:
    project_root: Path
    python_files: list[Path] = field(default_factory=list)
    relative_files: list[str] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)
    circular_import_candidates: list[tuple[str, str]] = field(default_factory=list)
    hardcoded_secret_candidates: list[str] = field(default_factory=list)
    wildcard_imports: list[str] = field(default_factory=list)
    missing_module_docstrings: list[str] = field(default_factory=list)
    missing_public_docstrings: list[str] = field(default_factory=list)
    oversized_modules: list[str] = field(default_factory=list)
    god_object_candidates: list[str] = field(default_factory=list)
    duplicate_namespace_candidates: list[tuple[str, str]] = field(default_factory=list)
    root_python_artifacts: list[str] = field(default_factory=list)
    mutable_default_candidates: list[str] = field(default_factory=list)
    broad_exception_candidates: list[str] = field(default_factory=list)
    print_statement_candidates: list[str] = field(default_factory=list)
    todo_candidates: list[str] = field(default_factory=list)
    noncanonical_runtime_imports: list[str] = field(default_factory=list)
    missing_tests: bool = False
    missing_readme: bool = False
    missing_pyproject: bool = False
    missing_constitution: bool = False
    missing_governance_docs: bool = False
    missing_span_package: bool = False

    def to_rule_context(self) -> dict[str, Any]:
        return {
            "project_root": str(self.project_root),
            "parse_errors": self.parse_errors,
            "circular_import_candidates": self.circular_import_candidates,
            "hardcoded_secret_candidates": self.hardcoded_secret_candidates,
            "wildcard_imports": self.wildcard_imports,
            "missing_module_docstrings": self.missing_module_docstrings,
            "missing_public_docstrings": self.missing_public_docstrings,
            "oversized_modules": self.oversized_modules,
            "god_object_candidates": self.god_object_candidates,
            "duplicate_namespace_candidates": self.duplicate_namespace_candidates,
            "root_python_artifacts": self.root_python_artifacts,
            "mutable_default_candidates": self.mutable_default_candidates,
            "broad_exception_candidates": self.broad_exception_candidates,
            "print_statement_candidates": self.print_statement_candidates,
            "todo_candidates": self.todo_candidates,
            "noncanonical_runtime_imports": self.noncanonical_runtime_imports,
            "missing_tests": self.missing_tests,
            "missing_readme": self.missing_readme,
            "missing_pyproject": self.missing_pyproject,
            "missing_constitution": self.missing_constitution,
            "missing_governance_docs": self.missing_governance_docs,
            "missing_span_package": self.missing_span_package,
        }


class ProjectInspector:
    """Build deterministic static-analysis context for Genesis 14 rules."""

    EXCLUDED_PARTS = {
        ".git", ".venv", "venv", "__pycache__", "node_modules",
        "dist", "build", ".mypy_cache", ".pytest_cache", "reports",
        "backups", "archive", "archives",
    }

    def inspect(self, project_root: str | Path) -> ProjectContext:
        root = Path(project_root).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            raise ValueError(f"project root does not exist or is not a directory: {root}")

        context = ProjectContext(project_root=root)
        context.python_files = sorted(self._python_files(root))
        context.relative_files = [str(path.relative_to(root)) for path in context.python_files]

        context.missing_tests = not any((root / name).exists() for name in ("tests", "test"))
        context.missing_readme = not any((root / name).exists() for name in ("README.md", "README.rst", "README"))
        context.missing_pyproject = not (root / "pyproject.toml").exists()
        context.missing_constitution = not self._any_exists(
            root, ("CONSTITUTION.md", "docs/CONSTITUTION.md", "docs/constitution.md")
        )
        context.missing_governance_docs = not self._any_exists(
            root, ("GOVERNANCE.md", "docs/GOVERNANCE.md", "docs/governance.md")
        )
        context.missing_span_package = not (root / "aletheus" / "span").exists()

        self._inspect_namespaces(root, context)
        self._inspect_root_artifacts(root, context)

        import_graph: dict[str, set[str]] = {}
        for path in context.python_files:
            self._inspect_file(root, path, context, import_graph)

        context.circular_import_candidates = self._two_way_edges(import_graph)
        return context

    def _python_files(self, root: Path) -> Iterable[Path]:
        for path in root.rglob("*.py"):
            if any(part in self.EXCLUDED_PARTS for part in path.parts):
                continue
            if path.is_file():
                yield path

    @staticmethod
    def _any_exists(root: Path, candidates: tuple[str, ...]) -> bool:
        return any((root / item).exists() for item in candidates)

    @staticmethod
    def _inspect_namespaces(root: Path, context: ProjectContext) -> None:
        candidates = (
            ("event_bus", "eventbus"),
            ("backup", "backups"),
            ("card_hawk", "cardhawk"),
            ("workflow", "workflows"),
            ("engine", "engines"),
            ("runtime", "runtimes"),
        )
        search_roots = [root, root / "aletheus"]
        for search_root in search_roots:
            if not search_root.exists():
                continue
            names = {p.name for p in search_root.iterdir() if p.is_dir()}
            for left, right in candidates:
                if left in names and right in names:
                    context.duplicate_namespace_candidates.append((left, right))

    @staticmethod
    def _inspect_root_artifacts(root: Path, context: ProjectContext) -> None:
        allow = {"setup.py", "manage.py", "conftest.py"}
        context.root_python_artifacts = sorted(
            p.name for p in root.glob("*.py")
            if p.name not in allow and not p.name.startswith(".")
        )

    def _inspect_file(
        self,
        root: Path,
        path: Path,
        context: ProjectContext,
        import_graph: dict[str, set[str]],
    ) -> None:
        rel = str(path.relative_to(root))
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            source = path.read_text(encoding="utf-8", errors="replace")

        lines = source.splitlines()
        if len(lines) > 900:
            context.oversized_modules.append(rel)

        for pattern in _SECRET_PATTERNS:
            if pattern.search(source):
                context.hardcoded_secret_candidates.append(rel)
                break

        if re.search(r"(?im)^\s*(TODO|FIXME|HACK)\b", source):
            context.todo_candidates.append(rel)

        try:
            tree = ast.parse(source, filename=rel)
        except SyntaxError as exc:
            context.parse_errors.append(f"{rel}:{exc.lineno}:{exc.offset}: {exc.msg}")
            return

        if ast.get_docstring(tree) is None and path.name != "__init__.py":
            context.missing_module_docstrings.append(rel)

        module_name = self._module_name(root, path)
        import_graph.setdefault(module_name, set())

        class_method_counts: list[tuple[str, int]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    import_graph[module_name].add(node.module)
                if any(alias.name == "*" for alias in node.names):
                    context.wildcard_imports.append(rel)
                if node.module and node.module.startswith("aletheus.runtime.core"):
                    if not rel.endswith("aletheus/runtime/core.py"):
                        context.noncanonical_runtime_imports.append(rel)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_graph[module_name].add(alias.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not node.name.startswith("_") and ast.get_docstring(node) is None:
                    context.missing_public_docstrings.append(f"{rel}:{node.lineno}:{node.name}")
                if isinstance(node, ast.ClassDef):
                    methods = sum(
                        isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                        for item in node.body
                    )
                    class_method_counts.append((node.name, methods))
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "print":
                    context.print_statement_candidates.append(f"{rel}:{node.lineno}")
            elif isinstance(node, ast.ExceptHandler):
                if node.type is None or (
                    isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}
                ):
                    context.broad_exception_candidates.append(f"{rel}:{node.lineno}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in (*node.args.defaults, *node.args.kw_defaults):
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        context.mutable_default_candidates.append(
                            f"{rel}:{node.lineno}:{node.name}"
                        )

        for class_name, methods in class_method_counts:
            if methods >= 35:
                context.god_object_candidates.append(f"{rel}:{class_name}:{methods}")

    @staticmethod
    def _module_name(root: Path, path: Path) -> str:
        parts = list(path.relative_to(root).with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts.pop()
        return ".".join(parts)

    @staticmethod
    def _two_way_edges(graph: dict[str, set[str]]) -> list[tuple[str, str]]:
        pairs: set[tuple[str, str]] = set()
        for source, targets in graph.items():
            for target in targets:
                if source in graph.get(target, set()):
                    pairs.add(tuple(sorted((source, target))))
        return sorted(pairs)

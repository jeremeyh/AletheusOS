"""AST-based Python dependency analyzer for SPAN™."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

from ..evidence import EvidenceStore
from ..graph import ArchitecturalGraph
from ..models import (
    AnalysisContext,
    AnalyzerResult,
    Evidence,
    Finding,
    FindingSeverity,
    Metric,
    SourceLocation,
)


class DependencyAnalyzer:
    """Discover Python module imports and identify dependency cycles."""

    name = "dependency"
    version = "1.0.0"

    def analyze(
        self,
        context: AnalysisContext,
        evidence: EvidenceStore,
        graph: ArchitecturalGraph,
    ) -> AnalyzerResult:
        result = AnalyzerResult(analyzer=self.name, version=self.version)
        parse_errors = 0
        scanned_files = 0
        import_count = 0

        module_paths = self._discover_modules(context)
        known_modules = {self._module_name(context.repository_root, path): path for path in module_paths}

        for module_name, path in known_modules.items():
            graph.ensure_node(
                module_name,
                kind="python_module",
                label=module_name,
                attributes={"path": str(path.relative_to(context.repository_root))},
            )

        for module_name, path in known_modules.items():
            scanned_files += 1
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, UnicodeDecodeError, SyntaxError) as exc:
                parse_errors += 1
                result.findings.append(
                    Finding(
                        analyzer=self.name,
                        category="parse_error",
                        title=f"Unable to parse {path.name}",
                        description=str(exc),
                        severity=FindingSeverity.MEDIUM,
                        recommendation="Correct the syntax or encoding issue so SPAN can analyze this module.",
                        attributes={"path": str(path)},
                    )
                )
                continue

            for imported, line in self._imports(tree, module_name):
                import_count += 1
                target = self._resolve_known_module(imported, known_modules)
                evidence_item = Evidence(
                    kind="python_import",
                    source=module_name,
                    target=target or imported,
                    location=SourceLocation.from_path(
                        path.relative_to(context.repository_root),
                        line=line,
                    ),
                    attributes={"resolved": target is not None, "raw_import": imported},
                )
                evidence.add(evidence_item)
                result.evidence.append(evidence_item)

                if target is not None:
                    graph.connect(
                        module_name,
                        target,
                        kind="imports",
                        attributes={"line": line, "evidence_id": evidence_item.id},
                    )

        cycles = graph.dependency_cycles(edge_kind="imports")
        for cycle in cycles:
            cycle_text = " → ".join((*cycle, cycle[0]))
            result.findings.append(
                Finding(
                    analyzer=self.name,
                    category="dependency_cycle",
                    title="Python dependency cycle detected",
                    description=cycle_text,
                    severity=FindingSeverity.HIGH,
                    recommendation="Break the cycle using an interface, event boundary, shared contract, or dependency inversion.",
                    attributes={"cycle": cycle},
                )
            )

        result.metrics.extend(
            [
                Metric("python_files_scanned", float(scanned_files)),
                Metric("python_imports_observed", float(import_count)),
                Metric("python_parse_errors", float(parse_errors)),
                Metric("dependency_cycles", float(len(cycles))),
            ]
        )
        return result.complete()

    def _discover_modules(self, context: AnalysisContext) -> tuple[Path, ...]:
        roots = context.include_paths or (Path("aletheus"),)
        discovered: list[Path] = []
        for relative_root in roots:
            root = relative_root if relative_root.is_absolute() else context.repository_root / relative_root
            if not root.exists():
                continue
            for path in root.rglob("*.py"):
                if any(part in context.exclude_names for part in path.parts):
                    continue
                discovered.append(path.resolve())
        return tuple(sorted(set(discovered)))

    @staticmethod
    def _module_name(repository_root: Path, path: Path) -> str:
        relative = path.relative_to(repository_root).with_suffix("")
        parts = list(relative.parts)
        if parts and parts[-1] == "__init__":
            parts.pop()
        return ".".join(parts)

    @staticmethod
    def _resolve_known_module(imported: str, known_modules: dict[str, Path]) -> str | None:
        candidate = imported
        while candidate:
            if candidate in known_modules:
                return candidate
            candidate = candidate.rpartition(".")[0]
        return None

    @staticmethod
    def _imports(tree: ast.AST, current_module: str) -> Iterable[tuple[str, int]]:
        package_parts = current_module.split(".")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    yield alias.name, node.lineno
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base_parts = package_parts[:-node.level]
                    if node.module:
                        base_parts.extend(node.module.split("."))
                    base = ".".join(base_parts)
                else:
                    base = node.module or ""
                if base:
                    yield base, node.lineno

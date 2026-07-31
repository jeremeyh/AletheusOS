from __future__ import annotations

import ast
from collections import defaultdict
from collections.abc import Iterable

from .models import AuditReport, ImportEdge, ParsedRuntimeModule

INTERNAL_RUNTIME_PREFIX = "aletheus.runtime"


def _resolve_relative_import(
    source_package: str,
    level: int,
    imported_module: str | None,
) -> str:
    """Resolve ImportFrom nodes into canonical absolute module names."""

    if level == 0:
        return imported_module or ""

    package_parts = source_package.split(".") if source_package else []

    # One leading dot means the current package. Each additional dot moves
    # upward by one package.
    parent_levels = max(level - 1, 0)

    if parent_levels:
        if parent_levels >= len(package_parts):
            package_parts = []
        else:
            package_parts = package_parts[:-parent_levels]

    if imported_module:
        package_parts.extend(imported_module.split("."))

    return ".".join(part for part in package_parts if part)


def _is_internal(target: str) -> bool:
    return target == INTERNAL_RUNTIME_PREFIX or target.startswith(
        f"{INTERNAL_RUNTIME_PREFIX}."
    )


def collect_import_edges(
    parsed_modules: Iterable[ParsedRuntimeModule],
) -> list[ImportEdge]:
    """Collect import relationships from parsed runtime modules."""

    edges: list[ImportEdge] = []

    for parsed in parsed_modules:
        if parsed.tree is None:
            continue

        source = parsed.module.name
        source_package = parsed.module.package

        for node in ast.walk(parsed.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = alias.name

                    edges.append(
                        ImportEdge(
                            source=source,
                            target=target,
                            line=node.lineno,
                            imported_name=alias.name,
                            internal=_is_internal(target),
                        )
                    )

            elif isinstance(node, ast.ImportFrom):
                target = _resolve_relative_import(
                    source_package=source_package,
                    level=node.level,
                    imported_module=node.module,
                )

                imported_names = ", ".join(alias.name for alias in node.names)

                edges.append(
                    ImportEdge(
                        source=source,
                        target=target,
                        line=node.lineno,
                        imported_name=imported_names,
                        internal=_is_internal(target),
                    )
                )

    return edges


def _normalize_internal_target(
    edge: ImportEdge,
    known_modules: set[str],
) -> str | None:
    """
    Resolve an import edge to the most specific known runtime module.

    For imports such as:

        from aletheus.runtime.kernel import RuntimeKernel

    first try:

        aletheus.runtime.kernel.RuntimeKernel

    and then fall back to:

        aletheus.runtime.kernel
    """

    candidates: list[str] = []

    for imported_name in (name.strip() for name in edge.imported_name.split(",")):
        if imported_name and imported_name != "*":
            candidates.append(f"{edge.target}.{imported_name}")

    candidates.append(edge.target)

    for original_candidate in candidates:
        candidate = original_candidate

        while candidate:
            if candidate in known_modules:
                return candidate

            if "." not in candidate:
                break

            candidate = candidate.rpartition(".")[0]

    return None


def build_internal_graph(
    imports: Iterable[ImportEdge],
    known_modules: set[str],
) -> dict[str, set[str]]:
    """Build the normalized internal runtime dependency graph."""

    graph: dict[str, set[str]] = {module_name: set() for module_name in known_modules}

    for edge in imports:
        if not edge.internal:
            continue

        target = _normalize_internal_target(
            edge,
            known_modules,
        )

        if target and target != edge.source:
            graph.setdefault(edge.source, set()).add(target)

    return graph


def detect_dependency_cycles(
    graph: dict[str, set[str]],
) -> list[list[str]]:
    """Detect unique directed cycles in the import graph."""

    cycles: set[tuple[str, ...]] = set()
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def canonicalize(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]

        if not body:
            return tuple(cycle)

        rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]

        canonical_body = min(rotations)

        return (*canonical_body, canonical_body[0])

    def visit(node: str) -> None:
        if node in visiting:
            try:
                start = stack.index(node)
            except ValueError:
                return

            cycle = stack[start:] + [node]
            cycles.add(canonicalize(cycle))
            return

        if node in visited:
            return

        visiting.add(node)
        stack.append(node)

        for dependency in sorted(graph.get(node, set())):
            visit(dependency)

        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for module_name in sorted(graph):
        visit(module_name)

    return [list(cycle) for cycle in sorted(cycles)]


def detect_orphan_modules(
    graph: dict[str, set[str]],
    ignored_modules: set[str] | None = None,
) -> list[str]:
    """Find modules with neither inbound nor outbound runtime imports."""

    ignored = ignored_modules or set()
    inbound: dict[str, int] = defaultdict(int)

    for dependencies in graph.values():
        for dependency in dependencies:
            inbound[dependency] += 1

    return sorted(
        module_name
        for module_name, dependencies in graph.items()
        if module_name not in ignored and not dependencies and inbound[module_name] == 0
    )


def analyze_imports(report: AuditReport) -> dict[str, set[str]]:
    """Populate import edges, cycles, and orphan-module observations."""

    report.imports = collect_import_edges(
        report.parsed_modules,
    )

    known_modules = {module.name for module in report.modules}

    graph = build_internal_graph(
        report.imports,
        known_modules,
    )

    report.dependency_cycles = detect_dependency_cycles(graph)

    report.orphan_modules = detect_orphan_modules(
        graph,
        ignored_modules={
            "aletheus.runtime",
            "aletheus.runtime.__main__",
        },
    )

    for cycle in report.dependency_cycles:
        report.add_finding(
            "error",
            "dependency_cycle",
            "Runtime dependency cycle detected: " + " -> ".join(cycle),
            cycle=cycle,
        )

    # Orphans are summarized rather than emitted as hundreds of individual
    # findings. The complete list remains available in report.orphan_modules.
    if report.orphan_modules:
        report.add_finding(
            "info",
            "orphan_modules",
            (
                f"{len(report.orphan_modules)} runtime modules have no "
                "internal inbound or outbound imports."
            ),
            count=len(report.orphan_modules),
        )

    return graph

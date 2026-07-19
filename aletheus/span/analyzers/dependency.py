"""
SPAN Dependency Analyzer v2

Consumes normalized import evidence from EvidenceStore.
"""

from __future__ import annotations

from collections import defaultdict

from aletheus.span.analyzer import Analyzer
from aletheus.span.finding import Finding, Severity


class DependencyAnalyzer(Analyzer):
    name = "dependency"
    version = "2.0.0"
    description = "Evidence-driven dependency analysis."

    required_evidence = (
        "import",
        "python_module",
    )

    def analyze(self, evidence, context):
        imports = evidence.query(kind="import")
        modules = evidence.query(kind="python_module")

        graph = defaultdict(set)
        reverse = defaultdict(set)

        known_modules = {
            rec.payload["module"]
            for rec in modules
            if "module" in rec.payload
        }

        for rec in imports:
            src = rec.payload.get("source_module")
            dst = rec.payload.get("target_module")

            if not src or not dst:
                continue

            graph[src].add(dst)
            reverse[dst].add(src)

        for module in sorted(known_modules):
            outgoing = len(graph[module])
            incoming = len(reverse[module])

            if outgoing == 0 and incoming == 0:
                yield Finding(
                    analyzer=self.name,
                    category="dependency",
                    title=f"Orphan module: {module}",
                    summary="Module has no incoming or outgoing dependencies.",
                    severity=Severity.LOW,
                    confidence=1.0,
                    recommendation="Review whether the module is still required.",
                    tags=("orphan",),
                )

            if outgoing > 25:
                yield Finding(
                    analyzer=self.name,
                    category="dependency",
                    title=f"High fan-out: {module}",
                    summary=f"Module depends on {outgoing} modules.",
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    recommendation="Reduce coupling through composition or abstraction.",
                    tags=("fan-out",),
                )

            if incoming > 40:
                yield Finding(
                    analyzer=self.name,
                    category="dependency",
                    title=f"High fan-in: {module}",
                    summary=f"{incoming} modules depend on this module.",
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    recommendation="Verify API stability and architectural responsibility.",
                    tags=("fan-in",),
                )

        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)
            stack.append(node)
            for nxt in graph[node]:
                if nxt in stack:
                    cycle = stack[stack.index(nxt):] + [nxt]
                    yield Finding(
                        analyzer=self.name,
                        category="dependency",
                        title="Circular dependency",
                        summary=" -> ".join(cycle),
                        severity=Severity.HIGH,
                        confidence=0.98,
                        recommendation="Break the dependency cycle.",
                        tags=("cycle",),
                    )
                elif nxt not in visited:
                    yield from dfs(nxt)
            stack.pop()

        for node in sorted(graph):
            if node not in visited:
                yield from dfs(node)

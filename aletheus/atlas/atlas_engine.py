from __future__ import annotations

import ast
import json
from datetime import datetime
from pathlib import Path


class AtlasEngine:
    """
    Atlas™

    Builds an architecture graph of the AletheusOS repository.

    Responsibilities:
    - discover Python modules
    - map imports
    - detect local dependency edges
    - find circular dependencies
    - identify duplicate package families
    - generate architecture reports
    """

    VERSION = "1.0.0"

    IGNORE_DIRS = {
        ".git",
        "venv",
        "__pycache__",
        "reports",
        "logs",
        "runtime_state",
        "uploads",
        "exports",
        "backups",
    }

    DUPLICATE_FAMILIES = [
        ("plugins", "plugins_v3"),
        ("planning", "planning_v2"),
        ("mission", "missions_v2"),
        ("workflow", "workflow_v3", "workflows", "workflows_v2"),
        ("event_bus", "eventbus"),
        ("hawk_aeye", "hawk_a_eye", "cardhawk_aeye"),
        ("thorx", "engine/thorx", "engines/thorx"),
    ]

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.report_dir = self.root / "reports" / "atlas"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self) -> dict:
        modules = self._discover_modules()
        imports = self._collect_imports(modules)
        edges = self._local_edges(modules, imports)
        cycles = self._detect_cycles(edges)
        duplicates = self._detect_duplicates()
        findings = self._findings(cycles, duplicates)

        result = {
            "atlas": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "root": str(self.root),
                "status": self._status(findings),
                "score": self._score(findings),
                "summary": {
                    "modules": len(modules),
                    "imports": sum(len(v) for v in imports.values()),
                    "local_edges": len(edges),
                    "cycles": len(cycles),
                    "duplicate_families": len(duplicates),
                },
                "modules": modules,
                "edges": edges,
                "cycles": cycles,
                "duplicates": duplicates,
                "findings": findings,
            }
        }

        self._write_reports(result)
        return result

    def _discover_modules(self) -> dict:
        modules = {}

        for path in self.root.rglob("*.py"):
            if self._ignored(path):
                continue

            rel = path.relative_to(self.root)
            module = ".".join(rel.with_suffix("").parts)

            if module.endswith(".__init__"):
                module = module[: -len(".__init__")]

            modules[module] = str(rel)

        return modules

    def _collect_imports(self, modules: dict) -> dict:
        imports = {}

        for module, rel_path in modules.items():
            path = self.root / rel_path
            found = []

            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except SyntaxError as exc:
                imports[module] = [{
                    "type": "syntax_error",
                    "module": "",
                    "message": f"{exc.msg} at line {exc.lineno}",
                }]
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        found.append({
                            "type": "import",
                            "module": alias.name,
                        })

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        found.append({
                            "type": "from",
                            "module": node.module,
                            "level": node.level,
                        })

            imports[module] = found

        return imports

    def _local_edges(self, modules: dict, imports: dict) -> list[dict]:
        module_names = set(modules.keys())
        edges = []

        top_level = {name.split(".")[0] for name in module_names}

        for source, source_imports in imports.items():
            for item in source_imports:
                target = item.get("module", "")

                if not target:
                    continue

                target_top = target.split(".")[0]

                if target in module_names or target_top in top_level:
                    edges.append({
                        "source": source,
                        "target": target,
                        "type": item.get("type", "import"),
                    })

        return edges

    def _detect_cycles(self, edges: list[dict]) -> list[list[str]]:
        graph = {}

        for edge in edges:
            graph.setdefault(edge["source"], set()).add(edge["target"])

        cycles = []
        visiting = set()
        visited = set()
        stack = []

        def visit(node):
            if node in visiting:
                try:
                    start = stack.index(node)
                    cycle = stack[start:] + [node]
                    if cycle not in cycles:
                        cycles.append(cycle)
                except ValueError:
                    pass
                return

            if node in visited:
                return

            visiting.add(node)
            stack.append(node)

            for neighbor in graph.get(node, []):
                if neighbor in graph:
                    visit(neighbor)

            stack.pop()
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node)

        return cycles[:50]

    def _detect_duplicates(self) -> list[dict]:
        duplicates = []

        for family in self.DUPLICATE_FAMILIES:
            present = []

            for name in family:
                path = self.root / name
                if path.exists():
                    present.append(name)

            if len(present) > 1:
                duplicates.append({
                    "family": family,
                    "present": present,
                    "message": "Multiple related architecture packages exist. Confirm canonical ownership before deleting.",
                })

        return duplicates

    def _findings(self, cycles: list, duplicates: list) -> list[dict]:
        findings = []

        if cycles:
            findings.append({
                "severity": "high",
                "code": "CIRCULAR_DEPENDENCIES",
                "message": f"{len(cycles)} circular dependency pattern(s) detected.",
            })

        if duplicates:
            findings.append({
                "severity": "medium",
                "code": "DUPLICATE_ARCHITECTURE_FAMILIES",
                "message": f"{len(duplicates)} duplicate architecture family/families detected.",
            })

        return findings

    def _score(self, findings: list[dict]) -> int:
        score = 100

        for finding in findings:
            severity = finding["severity"]
            if severity == "critical":
                score -= 30
            elif severity == "high":
                score -= 15
            elif severity == "medium":
                score -= 7
            elif severity == "low":
                score -= 2

        return max(score, 0)

    def _status(self, findings: list[dict]) -> str:
        severities = {finding["severity"] for finding in findings}

        if "critical" in severities:
            return "critical"
        if "high" in severities:
            return "degraded"
        if "medium" in severities or "low" in severities:
            return "watching"

        return "healthy"

    def _write_reports(self, result: dict):
        json_path = self.report_dir / "atlas_report.json"
        md_path = self.report_dir / "atlas_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

    def _markdown(self, result: dict) -> str:
        atlas = result["atlas"]

        lines = [
            "# Atlas™ Architecture Report",
            "",
            f"Generated: {atlas['timestamp']}",
            f"Status: **{atlas['status']}**",
            f"Score: **{atlas['score']}**",
            "",
            "## Summary",
            "",
        ]

        for key, value in atlas["summary"].items():
            lines.append(f"- {key}: {value}")

        lines.extend(["", "## Findings", ""])

        if not atlas["findings"]:
            lines.append("- No findings.")
        else:
            for finding in atlas["findings"]:
                lines.append(
                    f"- **[{finding['severity']}] {finding['code']}** — {finding['message']}"
                )

        lines.extend(["", "## Duplicate Families", ""])

        if not atlas["duplicates"]:
            lines.append("- None")
        else:
            for duplicate in atlas["duplicates"]:
                lines.append(f"- {', '.join(duplicate['present'])}")

        lines.extend(["", "## Cycles", ""])

        if not atlas["cycles"]:
            lines.append("- None")
        else:
            for cycle in atlas["cycles"][:20]:
                lines.append(f"- {' → '.join(cycle)}")

        return "\n".join(lines)

    def _ignored(self, path: Path) -> bool:
        return any(part in self.IGNORE_DIRS for part in path.parts)

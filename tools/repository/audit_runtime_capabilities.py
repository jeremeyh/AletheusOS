#!/usr/bin/env python3

from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]

EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "venv",
    "site-packages",
    "__pycache__",
    ".repository_backups",
    ".repository-quarantine",
    ".aletheus_restore_points",
    "node_modules",
}

CAPABILITIES: dict[str, tuple[str, ...]] = {
    "startup_boot": (
        "boot",
        "bootstrap",
        "startup",
        "start",
        "initialize",
        "initialization",
        "readiness",
        "lifecycle",
    ),
    "runtime_health": (
        "health",
        "liveness",
        "readiness",
        "diagnostic",
        "supervisor",
        "autonomic",
        "degraded",
    ),
    "dependency_topology": (
        "dependency",
        "dependencies",
        "graph",
        "topology",
        "atlas",
        "cycle",
        "dag",
    ),
    "capability_registration": (
        "capability",
        "registry",
        "register",
        "registration",
        "provider",
        "service registry",
        "engine registry",
    ),
    "configuration_validation": (
        "config",
        "configuration",
        "schema",
        "environment",
        "validate config",
        "settings",
    ),
    "constitutional_validation": (
        "constitutional",
        "constitution",
        "policy",
        "governance",
        "enforcement",
        "compliance",
        "audit",
    ),
    "observability": (
        "observability",
        "telemetry",
        "metrics",
        "runtime explorer",
        "runtime intelligence",
        "instrumentation",
    ),
    "resilience_recovery": (
        "recovery",
        "retry",
        "circuit breaker",
        "restart",
        "checkpoint",
        "graceful degradation",
        "fault tolerance",
    ),
}


@dataclass(frozen=True)
class Match:
    capability: str
    path: str
    score: int
    matched_terms: tuple[str, ...]
    classes: tuple[str, ...]
    functions: tuple[str, ...]
    imports: tuple[str, ...]


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in path.parts)


def python_files() -> Iterable[Path]:
    for path in ROOT.rglob("*.py"):
        if not is_excluded(path.relative_to(ROOT)):
            yield path


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def names_from_ast(text: str) -> tuple[list[str], list[str], list[str]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], [], []

    classes: list[str] = []
    functions: list[str] = []
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(module)

    return classes, functions, imports


def normalized_blob(
    path: Path,
    text: str,
    classes: list[str],
    functions: list[str],
    imports: list[str],
) -> str:
    symbols = " ".join(classes + functions + imports)
    blob = f"{path.as_posix()} {symbols} {text[:20000]}"
    return re.sub(r"[_\-]+", " ", blob.lower())


def inspect_file(path: Path) -> list[Match]:
    relative = path.relative_to(ROOT)
    text = safe_read(path)
    classes, functions, imports = names_from_ast(text)
    blob = normalized_blob(relative, text, classes, functions, imports)

    matches: list[Match] = []

    for capability, terms in CAPABILITIES.items():
        matched = tuple(sorted(term for term in terms if term in blob))
        if not matched:
            continue

        path_blob = relative.as_posix().lower().replace("_", " ")
        symbol_blob = " ".join(classes + functions).lower().replace("_", " ")

        score = len(matched)
        score += sum(3 for term in matched if term in path_blob)
        score += sum(2 for term in matched if term in symbol_blob)

        matches.append(
            Match(
                capability=capability,
                path=relative.as_posix(),
                score=score,
                matched_terms=matched,
                classes=tuple(classes[:20]),
                functions=tuple(functions[:30]),
                imports=tuple(imports[:20]),
            )
        )

    return matches


def main() -> int:
    grouped: dict[str, list[Match]] = defaultdict(list)

    for path in python_files():
        for match in inspect_file(path):
            grouped[match.capability].append(match)

    report: dict[str, object] = {
        "repository": str(ROOT),
        "capabilities": {},
    }

    markdown: list[str] = [
        "# AletheusOS Runtime Capability Reuse Audit",
        "",
        "Purpose: identify existing implementations before approving new builds.",
        "",
    ]

    for capability in CAPABILITIES:
        ranked = sorted(
            grouped.get(capability, []),
            key=lambda item: (-item.score, item.path),
        )

        high_signal = [item for item in ranked if item.score >= 5][:40]

        report["capabilities"][capability] = {
            "candidate_count": len(ranked),
            "high_signal_count": len(high_signal),
            "candidates": [asdict(item) for item in high_signal],
        }

        markdown.extend(
            [
                f"## {capability}",
                "",
                f"- All candidates: **{len(ranked)}**",
                f"- High-signal candidates: **{len(high_signal)}**",
                "",
            ]
        )

        if not high_signal:
            markdown.append("_No high-signal implementation found._")
            markdown.append("")
            continue

        markdown.append("| Score | Path | Matched terms |")
        markdown.append("|---:|---|---|")

        for item in high_signal:
            terms = ", ".join(item.matched_terms)
            markdown.append(f"| {item.score} | `{item.path}` | {terms} |")

        markdown.append("")

    output_dir = ROOT / "reports" / "architecture"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "runtime-capability-reuse-audit.json"
    markdown_path = output_dir / "runtime-capability-reuse-audit.md"

    json_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")

    print("AletheusOS Runtime Capability Reuse Audit")
    print("=" * 52)

    for capability in CAPABILITIES:
        candidates = report["capabilities"][capability]
        print(
            f"{capability:28} "
            f"{candidates['high_signal_count']:>3} high-signal candidates"
        )

    print()
    print(f"Markdown: {markdown_path.relative_to(ROOT)}")
    print(f"JSON:     {json_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

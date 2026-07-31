#!/usr/bin/env python3
"""
Genesis 7 Runtime Core Responsibility Audit

Analyzes aletheus/runtime/core.py and classifies methods by likely role:

- COMPOSITION
- BOOTSTRAP
- REGISTRATION
- DELEGATION
- OBSERVABILITY
- IMPLEMENTATION
- UNKNOWN

This audit is descriptive only. It does not modify runtime behavior.
"""

from __future__ import annotations

import ast
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

CORE_PATH = Path("aletheus/runtime/core.py")
REPORT_DIR = Path("reports/genesis_7_architecture_audit")
REPORT_PATH = REPORT_DIR / "runtime_core_responsibility_audit.md"


COMPOSITION_NAMES = {
    "__init__",
    "boot",
    "initialize",
    "startup",
    "shutdown",
    "wire",
    "compose",
    "attach",
}

REGISTRATION_TERMS = {
    "register",
    "registration",
    "bootstrap",
    "install",
    "attach",
    "bind",
}

DELEGATION_TERMS = {
    "dispatch",
    "execute",
    "delegate",
    "route",
    "submit",
    "handle",
}

OBSERVABILITY_TERMS = {
    "health",
    "status",
    "statistics",
    "stats",
    "metrics",
    "diagnostics",
    "report",
    "snapshot",
    "audit",
    "doctor",
    "validate",
}

IMPLEMENTATION_TERMS = {
    "create",
    "delete",
    "update",
    "predict",
    "reason",
    "remember",
    "recall",
    "plan",
    "forecast",
    "recommend",
    "authorize",
    "authenticate",
    "publish",
    "subscribe",
    "store",
    "search",
    "infer",
    "learn",
}


def call_name(node: ast.Call) -> str:
    func = node.func

    if isinstance(func, ast.Name):
        return func.id

    if isinstance(func, ast.Attribute):
        parts: list[str] = []
        current: ast.AST = func

        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value

        if isinstance(current, ast.Name):
            parts.append(current.id)

        return ".".join(reversed(parts))

    return "<dynamic>"


def classify_method(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[str, list[str]]:
    name = node.name.lower()
    reasons: list[str] = []

    if node.name in COMPOSITION_NAMES:
        reasons.append("recognized composition/lifecycle method")
        return "COMPOSITION", reasons

    calls = [call_name(item) for item in ast.walk(node) if isinstance(item, ast.Call)]

    self_assignments = 0
    for item in ast.walk(node):
        if not isinstance(item, (ast.Assign, ast.AnnAssign)):
            continue

        targets = item.targets if isinstance(item, ast.Assign) else [item.target]

        for target in targets:
            if (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                self_assignments += 1

    if any(term in name for term in REGISTRATION_TERMS):
        reasons.append("registration/bootstrap naming")
        return "REGISTRATION", reasons

    if name.startswith("_cmd_"):
        reasons.append("runtime command handler")
        return "IMPLEMENTATION", reasons

    if any(term in name for term in OBSERVABILITY_TERMS):
        reasons.append("observability or validation naming")
        return "OBSERVABILITY", reasons

    if any(term in name for term in IMPLEMENTATION_TERMS):
        reasons.append("domain behavior naming")
        return "IMPLEMENTATION", reasons

    delegated_calls = [
        call for call in calls if call.startswith("self.") and call.count(".") >= 2
    ]

    if delegated_calls and self_assignments == 0:
        reasons.append(
            f"delegates through attached components: {len(delegated_calls)} call(s)"
        )
        return "DELEGATION", reasons

    if self_assignments >= 2:
        reasons.append(f"wires runtime state: {self_assignments} self assignment(s)")
        return "COMPOSITION", reasons

    if len(node.body) <= 3 and calls:
        reasons.append("small forwarding method")
        return "DELEGATION", reasons

    reasons.append("manual review required")
    return "UNKNOWN", reasons


def source_span(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> int:
    end = getattr(node, "end_lineno", node.lineno)
    return end - node.lineno + 1


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source = CORE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(CORE_PATH))

    runtime_class: ast.ClassDef | None = None

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "AletheusRuntime":
            runtime_class = node
            break

    if runtime_class is None:
        raise SystemExit("Could not locate class AletheusRuntime in runtime/core.py")

    records: list[dict[str, object]] = []

    for node in runtime_class.body:
        if not isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            continue

        classification, reasons = classify_method(node)

        records.append(
            {
                "name": node.name,
                "line": node.lineno,
                "span": source_span(node),
                "classification": classification,
                "reasons": reasons,
            }
        )

    counts = Counter(str(record["classification"]) for record in records)

    total_lines = len(source.splitlines())
    implementation_lines = sum(
        int(record["span"])
        for record in records
        if record["classification"] == "IMPLEMENTATION"
    )
    unknown_lines = sum(
        int(record["span"])
        for record in records
        if record["classification"] == "UNKNOWN"
    )

    pressure_score = round(
        (implementation_lines + (unknown_lines * 0.5)) / max(total_lines, 1) * 100,
        2,
    )

    lines = [
        "# Genesis 7 Runtime Core Responsibility Audit",
        "",
        f"Generated: `{datetime.now(UTC).isoformat()}`",
        "",
        f"- File: `{CORE_PATH}`",
        f"- Total file lines: **{total_lines}**",
        f"- Runtime methods: **{len(records)}**",
        f"- Implementation-pressure score: **{pressure_score}%**",
        "",
        "## Responsibility Summary",
        "",
        "| Classification | Methods |",
        "|---|---:|",
    ]

    for classification in (
        "COMPOSITION",
        "REGISTRATION",
        "DELEGATION",
        "OBSERVABILITY",
        "IMPLEMENTATION",
        "UNKNOWN",
    ):
        lines.append(f"| {classification} | {counts.get(classification, 0)} |")

    lines.extend(
        [
            "",
            "## Method Classification",
            "",
            "| Method | Line | Lines | Classification | Reason |",
            "|---|---:|---:|---|---|",
        ]
    )

    for record in records:
        reason = "; ".join(record["reasons"])

        lines.append(
            f"| `{record['name']}` | "
            f"{record['line']} | "
            f"{record['span']} | "
            f"{record['classification']} | "
            f"{reason} |"
        )

    extraction_candidates = [
        record
        for record in records
        if record["classification"]
        in {
            "IMPLEMENTATION",
            "UNKNOWN",
        }
    ]

    extraction_candidates.sort(
        key=lambda item: int(item["span"]),
        reverse=True,
    )

    lines.extend(
        [
            "",
            "## Highest-Priority Extraction Candidates",
            "",
            "| Method | Classification | Lines | Recommended Direction |",
            "|---|---|---:|---|",
        ]
    )

    for record in extraction_candidates[:30]:
        name = str(record["name"])

        if name.startswith("_cmd_"):
            recommendation = (
                "Move handler logic into command-family component; "
                "retain thin compatibility delegate if needed"
            )
        elif record["classification"] == "UNKNOWN":
            recommendation = "Manual boundary review before architecture freeze"
        else:
            recommendation = (
                "Move domain behavior into bounded manager, service, engine, or façade"
            )

        lines.append(
            f"| `{name}` | "
            f"{record['classification']} | "
            f"{record['span']} | "
            f"{recommendation} |"
        )

    lines.extend(
        [
            "",
            "## Certification Interpretation",
            "",
            "- **0–10% pressure:** composition root is highly disciplined.",
            "- **10–20% pressure:** generally healthy; targeted extraction recommended.",
            "- **20–35% pressure:** meaningful implementation accumulation exists.",
            "- **Above 35%:** strong God Object pressure; freeze should be withheld.",
            "",
            "This score is a heuristic. Manual review remains authoritative.",
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(f"Runtime methods: {len(records)}")
    print(f"Core lines: {total_lines}")
    print(f"Implementation pressure: {pressure_score}%")
    print(
        "Implementation methods:",
        counts.get("IMPLEMENTATION", 0),
    )
    print("Unknown methods:", counts.get("UNKNOWN", 0))
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()

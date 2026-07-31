"""Dependency graph report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import DependencyGraphReport


def write_reports(
    report: DependencyGraphReport,
    output: Path,
) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "constitutional-dependency-graph.json"
    md_path = output / "constitutional-dependency-graph.md"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    relationship_counts: dict[str, int] = {}
    for relationship in report.relationships:
        relationship_counts[relationship.relationship] = (
            relationship_counts.get(relationship.relationship, 0) + 1
        )

    lines = [
        "# Kinekt™ Constitutional Dependency Graph",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Nodes: **{len(report.nodes)}**",
        f"- Relationships: **{len(report.relationships)}**",
        f"- Policy findings: **{len(report.findings)}**",
        f"- Unresolved modules: **{len(report.unresolved_modules)}**",
        "",
        "## Relationship counts",
        "",
    ]

    for relationship, count in sorted(relationship_counts.items()):
        lines.append(f"- `{relationship}`: **{count}**")

    lines.extend(["", "## Policy findings", ""])
    if report.findings:
        for finding in report.findings:
            lines.extend(
                [
                    f"### [{finding.severity.upper()}] {finding.code}",
                    "",
                    f"- Source: `{finding.source}`",
                    f"- Target: `{finding.target}`",
                    f"- {finding.message}",
                    f"- Evidence: {', '.join(finding.evidence) or 'none'}",
                    "",
                ]
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Unresolved modules", ""])
    for module in report.unresolved_modules[:200]:
        lines.append(f"- `{module}`")
    if len(report.unresolved_modules) > 200:
        lines.append(
            f"- ... {len(report.unresolved_modules) - 200} more in JSON report"
        )
    if not report.unresolved_modules:
        lines.append("- None")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

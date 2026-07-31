"""Kinekt™ report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import AnalysisResult


def write_reports(result: AnalysisResult, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    (output / "repository-intelligence.json").write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Repository Intelligence",
        "",
        f"- Root: `{result.root}`",
        f"- Generated: `{result.generated_at}`",
        f"- Modules: **{len(result.modules)}**",
        f"- Definitions: **{result.definition_count}**",
        f"- Findings: **{len(result.findings)}**",
        "",
        "## Package health",
        "",
    ]

    for metric in sorted(
        result.package_metrics,
        key=lambda item: (item.health_score, item.package),
    ):
        lines.append(
            f"- `{metric.package}` — health **{metric.health_score}**, "
            f"modules {metric.modules}, definitions {metric.definitions}, "
            f"fan-in {metric.internal_fan_in}, fan-out {metric.internal_fan_out}, "
            f"orphans {metric.orphan_candidates}, "
            f"duplicates {metric.duplicate_definitions}, "
            f"boundaries {metric.boundary_findings}"
        )

    lines.extend(["", "## Architectural findings", ""])
    if not result.findings:
        lines.append("No findings.")
    else:
        for finding in result.findings:
            lines.extend(
                [
                    f"### {finding.code}: `{finding.subject}`",
                    "",
                    f"- Severity: **{finding.severity}**",
                    f"- {finding.message}",
                    f"- Evidence: {', '.join(finding.evidence) or 'none'}",
                    "",
                ]
            )

    (output / "repository-intelligence.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

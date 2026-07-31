"""Runtime boundary report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import BoundaryReport


def write_reports(report: BoundaryReport, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "runtime-boundaries.json"
    md_path = output / "runtime-boundaries.md"
    seams_path = output / "boundary-seams.json"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    seams_path.write_text(
        json.dumps(
            {
                "generated_at": report.generated_at,
                "seams": [
                    {
                        "source": finding.source,
                        "target": finding.target,
                        "recommendation": finding.recommendation,
                    }
                    for finding in report.findings
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Runtime Boundary Analyzer",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Findings: **{len(report.findings)}**",
        f"- Unresolved relationships: **{report.unresolved_relationships}**",
        "",
        "## Findings",
        "",
    ]

    if report.findings:
        for finding in report.findings:
            lines.extend(
                [
                    f"### [{finding.severity.upper()}] {finding.code}",
                    "",
                    f"- Source: `{finding.source}` ({finding.source_layer})",
                    f"- Target: `{finding.target}` ({finding.target_layer})",
                    f"- {finding.message}",
                    f"- Recommendation: {finding.recommendation}",
                    f"- Evidence: {', '.join(finding.evidence) or 'none'}",
                    "",
                ]
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Lowest package boundary scores", ""])
    for package in report.package_pressure[:100]:
        lines.append(
            f"- `{package.package}` — score **{package.score:.2f}**, "
            f"status **{package.status}**, violations {package.violations}, "
            f"outbound {package.outbound_edges}, inbound {package.inbound_edges}"
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

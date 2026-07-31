"""Constitutional health report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import HealthReport


def write_reports(report: HealthReport, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "constitutional-health.json"
    md_path = output / "constitutional-health.md"
    executive_path = output / "executive-summary.json"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    executive_path.write_text(
        json.dumps(
            {
                "generated_at": report.generated_at,
                "total_score": report.total_score,
                "status": report.status,
                "readiness": report.readiness,
                "top_risks": report.top_risks[:10],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Constitutional Health",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Constitutional Health Index: **{report.total_score:.2f}**",
        f"- Status: **{report.status}**",
        f"- Readiness: **{report.readiness}**",
        "",
        "## Dimensions",
        "",
    ]

    for dimension in report.dimensions:
        lines.extend(
            [
                f"### {dimension.name}",
                "",
                f"- Score: **{dimension.score:.2f}**",
                f"- Weight: **{dimension.weight:.0%}**",
                f"- Status: **{dimension.status}**",
                f"- Evidence: {'; '.join(dimension.evidence) or 'none'}",
                f"- Risks: {'; '.join(dimension.risks) or 'none'}",
                "",
            ]
        )

    lines.extend(["## Top risks", ""])
    if report.top_risks:
        lines.extend(f"- {risk}" for risk in report.top_risks)
    else:
        lines.append("- None")

    lines.extend(["", "## Provenance", ""])
    for name, path in sorted(report.provenance.items()):
        lines.append(f"- `{name}`: `{path}`")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

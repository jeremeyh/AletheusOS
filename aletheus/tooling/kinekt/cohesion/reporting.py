"""Repository cohesion report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import CohesionReport


def write_reports(report: CohesionReport, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "repository-cohesion.json"
    md_path = output / "repository-cohesion.md"
    hotspots_path = output / "cohesion-hotspots.json"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    hotspots_path.write_text(
        json.dumps(
            {
                "generated_at": report.generated_at,
                "hotspots": report.hotspots,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Repository Cohesion",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Average score: **{report.average_score:.2f}**",
        f"- Status: **{report.status}**",
        f"- Packages: **{len(report.packages)}**",
        f"- Hotspots: **{len(report.hotspots)}**",
        "",
        "## Lowest-scoring packages",
        "",
    ]

    for package in report.packages[:100]:
        lines.extend(
            [
                f"### `{package.package}`",
                "",
                f"- Score: **{package.score:.2f}**",
                f"- Status: **{package.status}**",
                f"- Modules: {package.modules}",
                f"- Internal edges: {package.internal_edges}",
                f"- Isolated modules: {package.isolated_modules}",
                f"- Capabilities: {package.capability_count}",
                f"- Owners: {package.owner_count}",
                (
                    "- Recommendations: "
                    + ("; ".join(package.recommendations) or "none")
                ),
                "",
            ]
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

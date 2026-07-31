"""Integrity report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import IntegrityReport


def write_reports(report: IntegrityReport, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "platform-integrity.json"
    md_path = output / "platform-integrity.md"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Platform Integrity",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Total score: **{report.total_score:.2f}**",
        f"- Status: **{report.status}**",
        f"- Trend: **{report.trend}**",
        f"- Previous score: **{report.previous_score if report.previous_score is not None else 'none'}**",
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
                f"- Status: **{dimension.status}**",
                f"- Deductions: {', '.join(dimension.deductions) or 'none'}",
                "",
            ]
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

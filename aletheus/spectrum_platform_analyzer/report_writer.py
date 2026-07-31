"""
Spectrum Platform Analyzer
Report Writer

Genesis 54.1
"""

from __future__ import annotations

import json
from pathlib import Path


class ReportWriter:
    VERSION = "1.0.0"

    GENESIS = "54.1"

    def __init__(self, output_directory="reports/spectrum"):

        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write_json(self, report):

        filename = self.output_directory / f"{report.report_id}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                report.to_dict(),
                f,
                indent=4,
            )

        return filename

    def write_markdown(self, report):

        filename = self.output_directory / f"{report.report_id}.md"

        lines = []

        lines.append("# Spectrum Platform Analysis Report")
        lines.append("")
        lines.append(f"Report ID: **{report.report_id}**")
        lines.append("")
        lines.append(f"Generated: {report.generated_at}")
        lines.append("")

        lines.append("## Platform Score")
        lines.append("")

        score = report.score

        lines.append(f"- Overall: {score.overall():.2f}")
        lines.append(f"- Architecture: {score.architecture}")
        lines.append(f"- Maintainability: {score.maintainability}")
        lines.append(f"- Coupling: {score.coupling}")
        lines.append(f"- Boundaries: {score.boundaries}")
        lines.append(f"- Constitutional: {score.constitutional}")
        lines.append(f"- Security: {score.security}")
        lines.append(f"- Health: {score.health}")

        lines.append("")
        lines.append("## Findings")
        lines.append("")

        if not report.findings:
            lines.append("No findings.")

        else:
            for finding in report.findings:
                lines.append(f"### {finding.severity} — {finding.title}")

                lines.append("")
                lines.append(f"Component: `{finding.component}`")
                lines.append("")
                lines.append(finding.description)
                lines.append("")
                lines.append(f"Recommendation: {finding.recommendation}")
                lines.append("")

        filename.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return filename

    def health(self):

        return {
            "name": "Spectrum Report Writer",
            "status": "healthy",
            "version": self.VERSION,
            "genesis": self.GENESIS,
        }


report_writer = ReportWriter()

"""Runtime topology report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import TopologyReport


def write_reports(report: TopologyReport, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "runtime-topology.json"
    md_path = output / "runtime-topology.md"

    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Runtime Topology",
        "",
        f"- Generated: `{report.generated_at}`",
        f"- Source: `{report.source_report}`",
        f"- Modules: **{len(report.modules)}**",
        f"- Packages: **{len(report.packages)}**",
        f"- Entry-point candidates: **{len(report.entry_points)}**",
        f"- Sinks: **{len(report.sinks)}**",
        f"- Isolated modules: **{len(report.isolated)}**",
        f"- Cycle groups: **{len(report.cycles)}**",
        "",
        "## Longest chains",
        "",
    ]

    if report.longest_chains:
        for chain in report.longest_chains:
            lines.append(f"- {' → '.join(chain)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Cycle groups", ""])
    if report.cycles:
        for cycle in report.cycles:
            lines.append(f"- {', '.join(cycle)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Package topology", ""])
    for package in report.packages:
        lines.append(
            f"- `{package.package}` — modules {package.modules}, "
            f"internal edges {package.internal_edges}, "
            f"inbound packages {len(package.inbound_packages)}, "
            f"outbound packages {len(package.outbound_packages)}, "
            f"cycle groups {package.cycle_groups}, "
            f"isolated modules {package.isolated_modules}"
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

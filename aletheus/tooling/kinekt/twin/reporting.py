"""Twin report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import TwinSnapshot


def write_reports(snapshot: TwinSnapshot, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "architectural-digital-twin.json"
    md_path = output / "architectural-digital-twin.md"

    json_path.write_text(
        json.dumps(snapshot.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Architectural Digital Twin",
        "",
        f"- Snapshot: `{snapshot.snapshot_id}`",
        f"- Commit: `{snapshot.repository_commit}`",
        f"- Nodes: **{len(snapshot.nodes)}**",
        f"- Relationships: **{len(snapshot.relationships)}**",
        f"- Change status: **{snapshot.changes.get('status', 'unknown')}**",
        "",
        "## Metrics",
        "",
    ]
    for name, value in sorted(snapshot.metrics.items()):
        lines.append(f"- `{name}`: **{value}**")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

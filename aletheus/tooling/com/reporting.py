from __future__ import annotations

import json
from pathlib import Path

from .models import CognitiveMeshReport


def write_reports(report: CognitiveMeshReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "cognitive-mesh.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Aletheus Cognitive Operations Mesh™",
        "",
        f"- Contributions: **{len(report.contributions)}**",
        f"- Consensus records: **{len(report.consensus)}**",
        f"- Unresolved topics: **{len(report.unresolved_topics)}**",
    ]
    (output / "cognitive-mesh.md").write_text("\n".join(lines), encoding="utf-8")

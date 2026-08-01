from __future__ import annotations

import json
from pathlib import Path

from .models import MissionControlReport


def write_reports(report: MissionControlReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "mission-control.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output / "command-manifest.json").write_text(
        json.dumps(
            {
                "readiness": report.readiness,
                "commands_enabled": False,
                "missions": [
                    {
                        "mission_id": mission.mission_id,
                        "status": mission.status,
                        "approval_required": mission.approval_required,
                    }
                    for mission in report.missions
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Aletheus Mission Control™",
        "",
        f"- Readiness: **{report.readiness}**",
        f"- Missions: **{len(report.missions)}**",
        f"- Blocked reasons: **{len(report.blocked_reasons)}**",
        "",
        "## Missions",
        "",
    ]
    lines.extend(
        f"- `{mission.mission_id}` — {mission.title} ({mission.status})"
        for mission in report.missions
    )
    (output / "mission-control.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

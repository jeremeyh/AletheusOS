"""Evolution result reporting."""

from __future__ import annotations

import json
from pathlib import Path

from .models import EvolutionResult


def write_result(result: EvolutionResult, output: Path) -> tuple[Path, Path]:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / f"{result.plan_id}-{result.mode}.json"
    md_path = output / f"{result.plan_id}-{result.mode}.md"

    json_path.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Repository Evolution",
        "",
        f"- Plan: `{result.plan_id}`",
        f"- Mode: **{result.mode}**",
        f"- Status: **{result.status}**",
        f"- Backup: `{result.backup_directory or 'none'}`",
        f"- Rollback manifest: `{result.rollback_manifest or 'none'}`",
        "",
        "## Changed paths",
        "",
    ]
    lines.extend(f"- `{path}`" for path in result.changed_paths)
    if not result.changed_paths:
        lines.append("- None")

    lines.extend(["", "## Validation commands", ""])
    for command in result.commands:
        joined_command = " ".join(command.command)
        lines.append(f"- `{joined_command}` → return code {command.returncode}")

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in result.notes)
    if not result.notes:
        lines.append("- None")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path

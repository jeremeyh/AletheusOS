"""Orchestration report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ExecutionManifest


def write_reports(manifest: ExecutionManifest, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    (output / "execution-manifest.json").write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    (output / "rollback-plan.json").write_text(
        json.dumps(
            {
                "generated_at": manifest.generated_at,
                "units": [
                    {
                        "unit_id": unit.unit_id,
                        "rollback_requirements": list(unit.rollback_requirements),
                    }
                    for unit in manifest.units
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    (output / "validation-plan.json").write_text(
        json.dumps(
            {
                "generated_at": manifest.generated_at,
                "units": [
                    {
                        "unit_id": unit.unit_id,
                        "validations": list(unit.validations),
                    }
                    for unit in manifest.units
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Evolution Orchestration",
        "",
        f"- Status: **{manifest.status}**",
        f"- Execution units: **{len(manifest.units)}**",
        f"- Abstentions: **{len(manifest.abstentions)}**",
        "",
        "## Execution sequence",
        "",
    ]

    for unit in manifest.units:
        lines.extend(
            [
                f"### Phase {unit.phase}: {unit.title}",
                "",
                f"- Unit: `{unit.unit_id}`",
                f"- Category: `{unit.category}`",
                f"- Risk: **{unit.risk}**",
                f"- Effort: **{unit.effort}**",
                f"- Expected health gain: **+{unit.expected_health_gain:.2f}**",
                f"- Approval required: **{unit.approval_required}**",
                f"- Candidates: {', '.join(unit.candidate_ids)}",
                "",
            ]
        )

    lines.extend(["## Abstentions", ""])
    lines.extend(f"- {item}" for item in manifest.abstentions)
    if not manifest.abstentions:
        lines.append("- None")

    (output / "evolution-orchestration.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

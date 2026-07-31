"""Optimization report generation."""

from __future__ import annotations

import json
from pathlib import Path

from .models import OptimizationPlan


def write_reports(plan: OptimizationPlan, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    (output / "optimization-roadmap.json").write_text(
        json.dumps(plan.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output / "work-packages.json").write_text(
        json.dumps(
            {
                "generated_at": plan.generated_at,
                "work_packages": [
                    {
                        "package_id": item.package_id,
                        "title": item.title,
                        "phase": item.phase,
                        "category": item.category,
                        "estimated_effort": item.estimated_effort,
                        "risk": item.risk,
                        "expected_health_gain": item.expected_health_gain,
                        "candidate_ids": list(item.candidate_ids),
                    }
                    for item in plan.work_packages
                ],
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (output / "quick-wins.json").write_text(
        json.dumps(
            {"generated_at": plan.generated_at, "quick_wins": plan.quick_wins},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    lines = [
        "# Kinekt™ Optimization Roadmap",
        "",
        f"- Current health score: **{plan.current_health_score:.2f}**",
        f"- Readiness: **{plan.readiness}**",
        f"- Candidates: **{len(plan.candidates)}**",
        f"- Work packages: **{len(plan.work_packages)}**",
        f"- Quick wins: **{len(plan.quick_wins)}**",
        "",
        "## Implementation phases",
        "",
    ]
    for package in plan.work_packages:
        lines.extend(
            [
                f"### Phase {package.phase}: {package.title}",
                "",
                f"- Effort: **{package.estimated_effort}**",
                f"- Risk: **{package.risk}**",
                f"- Expected health gain: **+{package.expected_health_gain:.2f}**",
                f"- Candidates: {', '.join(package.candidate_ids)}",
                "",
            ]
        )
    lines.extend(["## Quick wins", ""])
    lines.extend(f"- `{item}`" for item in plan.quick_wins)
    if not plan.quick_wins:
        lines.append("- None")
    lines.extend(["", "## Abstentions", ""])
    lines.extend(f"- {item}" for item in plan.abstentions)
    if not plan.abstentions:
        lines.append("- None")

    (output / "optimization-roadmap.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

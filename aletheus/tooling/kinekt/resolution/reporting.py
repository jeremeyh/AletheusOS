"""Report generation for Kinekt™ finding resolution."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ResolutionReport

_TIER_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "suppressed": 4,
}


def write_reports(report: ResolutionReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    (output / "finding-resolution.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    counts = report.count_by_tier()
    lines = [
        "# Kinekt™ Finding Resolution",
        "",
        f"- Source: `{report.source_report}`",
        f"- Generated: `{report.generated_at}`",
        f"- Total items: **{len(report.items)}**",
        "",
        "## Triage summary",
        "",
    ]

    for tier in ("critical", "high", "medium", "low", "suppressed"):
        lines.append(f"- {tier}: **{counts.get(tier, 0)}**")

    actionable = [item for item in report.items if item.tier != "suppressed"]
    actionable.sort(
        key=lambda item: (
            _TIER_ORDER.get(item.tier, 99),
            -item.confidence,
            item.code,
            item.subject,
        )
    )

    lines.extend(["", "## Actionable findings", ""])
    if not actionable:
        lines.append("No actionable findings.")
    else:
        for item in actionable:
            lines.extend(
                [
                    f"### [{item.tier.upper()}] {item.code}: `{item.subject}`",
                    "",
                    f"- Confidence: **{item.confidence:.0%}**",
                    f"- Disposition: `{item.disposition}`",
                    f"- Recommendation: {item.recommendation}",
                    f"- Rationale: {'; '.join(item.rationale)}",
                    f"- Evidence: {', '.join(item.evidence) or 'none'}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Suppression",
            "",
            (
                "Suppressed findings remain present in the JSON report for traceability "
                "but do not dominate the actionable architecture queue."
            ),
            "",
        ]
    )

    (output / "finding-resolution.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

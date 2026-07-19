#!/usr/bin/env python3
"""Repository report rendering."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
import json

from .metrics import RepositoryMetrics
from .rules import PolicyViolation


def render_markdown(
    metrics: RepositoryMetrics,
    violations: Iterable[PolicyViolation],
    root: Path | str,
) -> str:
    violation_list = list(violations)
    generated = datetime.now(timezone.utc).isoformat()

    lines = [
        "# AletheusOS Repository Health Report",
        "",
        f"- Generated: `{generated}`",
        f"- Repository: `{Path(root).resolve()}`",
        f"- Health score: **{metrics.health_score:.2f}%**",
        "",
        "## Metrics",
        "",
        f"- Total files: **{metrics.total_files}**",
        f"- Python files: **{metrics.python_files}**",
        f"- Shell files: **{metrics.shell_files}**",
        f"- Documentation files: **{metrics.documentation_files}**",
        f"- Zero-byte files: **{metrics.zero_byte_files}**",
        f"- Root files: **{metrics.root_files}**",
        f"- Policy errors: **{metrics.policy_errors}**",
        f"- Policy warnings: **{metrics.policy_warnings}**",
        "",
        "## Violations",
        "",
    ]

    if not violation_list:
        lines.append("No structural policy violations detected.")
    else:
        for violation in violation_list:
            lines.extend(
                [
                    f"### {violation.code}: `{violation.path}`",
                    "",
                    f"- Severity: **{violation.severity}**",
                    f"- Problem: {violation.message}",
                    f"- Recommendation: {violation.recommendation}",
                    "",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def write_reports(
    output_directory: Path | str,
    metrics: RepositoryMetrics,
    violations: Iterable[PolicyViolation],
    root: Path | str,
) -> tuple[Path, Path]:
    destination = Path(output_directory)
    destination.mkdir(parents=True, exist_ok=True)

    violation_list = list(violations)
    markdown_path = destination / "repository-health.md"
    json_path = destination / "repository-health.json"

    markdown_path.write_text(
        render_markdown(metrics, violation_list, root),
        encoding="utf-8",
    )

    payload = {
        "root": str(Path(root).resolve()),
        "metrics": metrics.to_dict(),
        "violations": [
            {
                "code": item.code,
                "severity": item.severity,
                "path": str(item.path),
                "message": item.message,
                "recommendation": item.recommendation,
            }
            for item in violation_list
        ],
    }

    json_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    return markdown_path, json_path

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import ObservatoryReport


def write_reports(report: ObservatoryReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "platform-observatory.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output / "dashboard-metrics.json").write_text(
        json.dumps(
            {
                "health_score": report.health_score,
                "readiness": report.readiness,
                "authority_coverage": report.authority_coverage,
                "unresolved_modules": report.unresolved_modules,
                "execution_units": report.execution_units,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (output / "alerts.json").write_text(
        json.dumps(
            {"alerts": [asdict(alert) for alert in report.alerts]},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    lines = [
        "# Aletheus Observatory™",
        "",
        f"- Health score: **{report.health_score:.2f}**",
        f"- Readiness: **{report.readiness}**",
        f"- Authority coverage: **{report.authority_coverage:.2f}%**",
        f"- Unresolved modules: **{report.unresolved_modules}**",
        f"- Execution units: **{report.execution_units}**",
        f"- Alerts: **{len(report.alerts)}**",
    ]
    (output / "platform-observatory.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

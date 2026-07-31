"""Kinekt™ finding resolution engine."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import ResolutionReport
from .policy import ResolutionPolicy
from .reporting import write_reports
from .scoring import resolve_finding


class FindingResolutionEngine:
    """Resolve raw Kinekt findings into prioritized architectural work."""

    def __init__(
        self,
        source: Path,
        output: Path,
        policy: ResolutionPolicy | None = None,
    ) -> None:
        self.source = source.resolve()
        self.output = output.resolve()
        self.policy = policy or ResolutionPolicy()

    def run(self) -> ResolutionReport:
        payload: dict[str, Any] = json.loads(self.source.read_text(encoding="utf-8"))

        raw_findings = payload.get("findings", [])

        if not isinstance(raw_findings, list):
            raise TypeError(
                "Kinekt source report must contain a list named 'findings'."
            )

        items = [
            resolve_finding(finding, self.policy)
            for finding in raw_findings
            if isinstance(finding, dict)
        ]

        items.sort(
            key=lambda item: (
                item.tier,
                -item.confidence,
                item.code,
                item.subject,
            )
        )

        report = ResolutionReport(
            source_report=str(self.source),
            generated_at=datetime.now(UTC).isoformat(),
            items=items,
        )

        write_reports(report, self.output)

        return report

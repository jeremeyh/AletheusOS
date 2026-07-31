"""Kinekt™ Platform Integrity engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_json
from .models import IntegrityReport
from .reporting import write_reports
from .scoring import score_package_health, score_repository, score_resolution
from .trend import compare_previous


def _status(score: float) -> str:
    if score >= 90:
        return "healthy"
    if score >= 75:
        return "watch"
    if score >= 60:
        return "degraded"
    return "critical"


class IntegrityEngine:
    def __init__(
        self,
        repository_report: Path,
        resolution_report: Path,
        output: Path,
        baseline: Path | None = None,
    ) -> None:
        self.repository_report = repository_report.resolve()
        self.resolution_report = resolution_report.resolve()
        self.output = output.resolve()
        self.baseline = baseline.resolve() if baseline else None

    def analyze(self) -> IntegrityReport:
        repository = load_json(self.repository_report)
        resolution = load_json(self.resolution_report)

        dimensions = [
            *score_repository(repository),
            score_resolution(resolution),
            score_package_health(repository),
        ]
        total = round(
            sum(dimension.score for dimension in dimensions) / len(dimensions),
            2,
        )
        trend, previous_score = compare_previous(total, self.baseline)

        report = IntegrityReport(
            generated_at=datetime.now(UTC).isoformat(),
            source_repository_report=str(self.repository_report),
            source_resolution_report=str(self.resolution_report),
            total_score=total,
            status=_status(total),
            dimensions=dimensions,
            trend=trend,
            previous_score=previous_score,
        )
        write_reports(report, self.output)
        return report

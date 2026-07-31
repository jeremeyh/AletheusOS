"""Kinekt™ Repository Cohesion engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .analysis import analyze_packages
from .loader import load_object
from .models import CohesionReport
from .reporting import write_reports


def _status(score: float) -> str:
    if score >= 90:
        return "cohesive"
    if score >= 75:
        return "watch"
    if score >= 60:
        return "fragmented"
    return "critical"


class CohesionEngine:
    def __init__(
        self,
        topology_report: Path,
        dependency_report: Path,
        output: Path,
    ) -> None:
        self.topology_report = topology_report.resolve()
        self.dependency_report = dependency_report.resolve()
        self.output = output.resolve()

    def analyze(self) -> CohesionReport:
        topology = load_object(self.topology_report)
        dependency = load_object(self.dependency_report)
        packages = analyze_packages(topology, dependency)

        average = (
            round(
                sum(package.score for package in packages) / len(packages),
                2,
            )
            if packages
            else 0.0
        )

        hotspots = [
            package.package
            for package in packages
            if package.status in {"critical", "fragmented"}
        ]

        report = CohesionReport(
            generated_at=datetime.now(UTC).isoformat(),
            topology_report=str(self.topology_report),
            dependency_report=str(self.dependency_report),
            average_score=average,
            status=_status(average),
            packages=packages,
            hotspots=hotspots,
        )
        write_reports(report, self.output)
        return report
